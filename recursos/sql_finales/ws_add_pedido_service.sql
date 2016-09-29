CREATE OR REPLACE FUNCTION ws_add_pedido_service(_json json)
  RETURNS text AS
$BODY$
declare
	x record;
	y record;
	tem json;
	t text;
	id_emp text;
	ot text;
	id_inser integer;
	error text:='';
	stop boolean :=true;
	val_item boolean;
	id_pedido integer;
	cont_pedido text:='';
	ban_pedido boolean :=true;
	l json;
	ban_val_ind_emp boolean;
	tiempo_pedido numeric;
	tienda record;
	configuracion record;
	gen_nom_ped text;
	gen_nom_emp text;
	get_nom_arra text[];
begin
		for x in select * from json_array_elements(_json::json->'pedido') loop
			id_emp :=cast(x."value"::json->>'tienda' as json)->>'identificador'::text;
			select id::text,ciudad_id from usuario_tienda where id = case when id_emp ~ '^[0-9]+$' then cast(id_emp as integer) else 0 end limit 1 into tienda;
			if tienda is not null then
				val_item:=true;
				<<uno>>
				for y in select nombre,case when cantidad~'^([0-9]+[.])?[0-9]+' then true else false end as cantidad,case when valor~'^([0-9]+[.])?[0-9]+' then true else false end as valor from json_populate_recordset(null::ws_descripcion,cast(x."value"::json->>'descripcion' as json)) loop
					if not y.cantidad or not y.valor then
						val_item:=false;
						exit uno;
					end if;
				end loop;
				if val_item then
					/*+++ Generar el nombre del pedido ws */
					select num_pedido from pedido_pedidows where tienda_id= cast(tienda.id as integer) order by id desc limit 1 into gen_nom_ped;
					gen_nom_ped:= case when gen_nom_ped is null then null when length(gen_nom_ped)=0 then null else gen_nom_ped end;
					if gen_nom_ped is not null then
						select num_pedido from pedido_pedidows order by id desc limit 1 into gen_nom_ped;
						get_nom_arra:=string_to_array(gen_nom_ped,'_');
						gen_nom_emp:=get_nom_arra[1]||'_'||(cast(get_nom_arra[2] as integer) +1);
					else
						select e.first_name from usuario_tienda as t inner join usuario_empresa as e on (t.empresa_id=e.id and t.id=cast(tienda.id as integer)) limit 1 into gen_nom_emp;
						gen_nom_emp :=  left(upper(gen_nom_emp), 2)||'WS_1';
					end if;
					/*+++++++++++++++++*/
					select c.gps from usuario_tienda as t inner join usuario_empresa as e on (t.empresa_id=e.id and t.id=2) inner join pedido_configuraciontiempo as c on (c.empresa_id=e.id) limit 1 into configuracion;
					insert into pedido_pedidows (activado,detalle,num_pedido,npedido_express,cliente,fecha_pedido,tienda_id,tipo_pago,total,entregado,despachado,confirmado,alistado)
					values	(True,x."value",gen_nom_emp,gen_nom_emp,x."value"::json->>'cliente',now(),cast(tienda.id as integer),case when x."value"::json->>'tipo_pago'= '1' then 'Efectivo' when x."value"::json->>'tipo_pago' = '2' then 'Tarjeta' else 'Remision' end,cast(x."value"::json->>'total_pedido' as numeric),false,false,false,false)RETURNING id into id_inser;
					insert into pedido_timews(creado,pedido_id) values (now(),id_inser);
					SELECT COALESCE(array_to_json(array_agg(row_to_json(p))), '[]') from (
						select id,nit,direccion,latitud,longitud,referencia,celular,fijo from usuario_tienda where id = cast(tienda.id as integer) limit 1
					) p into l;
					cont_pedido:=cont_pedido||case when not ban_pedido then ',' else''end||'{"tiempo_gps":'||case when configuracion.gps is not null then configuracion.gps*1000 else 100 end||',"id":'||id_inser||',"ciudad":'||tienda.ciudad_id||',"tienda":'||l||',"info":'||x."value"::json||'}';
					ban_pedido:=false;
				else
					error:=error||case when not stop then ',' else''end||x."value"::json;
				end if;
			else
				error:=error||case when not stop then ',' else''end||x."value"::json;
				stop:=false;
			end if;

		end loop;
		select last(pedido)*10000 from pedido_configuraciontiempo into tiempo_pedido;
		return '{"respuesta":true,"error":['||error||'],"pedidos":['||cont_pedido||'],"retardo":'||tiempo_pedido||'}';
EXCEPTION WHEN others THEN
		return '{"respuesta":false,"mensage":"Error en la estructura del json"}';
end;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION ws_add_pedido_service(json)
  OWNER TO postgres;

select ws_add_pedido_service('')

{
        "pedido": [{
            "id": "ws_ped",
            "cliente": {
                "nombre": "mirlan",
                "apellidos": "Reyes Polo",
                "identificacion": "45454545454",
                "direccion": "dsdsdsdsddsdsdsdsdssds",
                "celular":"366454545",
                "fijo":"6605648"
            },
            "tienda": {
                "identificador": "3"
            },
            "descripcion": [{
                "nombre": "jajaja",
                "cantidad": 5,
                "valor": 1000
            }, {
                "nombre": "jajaja",
                "cantidad": 5,
                "valor": 1000
            }],
            "total_pedido": 50000,
            "tipo_pago": 1
        }, {
            "id": "ws_ped",
            "cliente": {
                "nombre": "mirlan",
                "apellidos": "Reyes Polo",
                "identificacion": "45454545454","direccion": "dsdsdsdsddsdsdsdsdssds","celular":"366454545","fijo":"6605648"},"tienda": {"identificador": "123456"},"descripcion": [{"nombre": "jajaja","cantidad": 5,"valor": 1000}, {"nombre": "jajaja","cantidad": 5,"valor": 1000}],"total_pedido": 50000,"tipo_pago": 1}]}