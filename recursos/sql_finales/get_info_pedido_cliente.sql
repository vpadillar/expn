select * from pedido_pedido order by id desc limit 5
select * from pedido_time
select * from usuario_cliente
update pedido_time set entregado=now()
 select get_info_pedido_cliente('Ol_4')
create or replace function get_info_pedido_cliente(nom_pedido text) returns text as $$
declare
 info json;
 res boolean;
begin
    select 'OL_4'~'([a-z]*[A-Z]*){0,2}_([0-9])+' into res;
    if res then
    	SELECT COALESCE(array_to_json(array_agg(row_to_json(p2))), '[]') from (
            select c.first_name||' '||c.last_name as cliente,
                    case when t.creado is not null then to_char(t.creado, 'DD/MM/YYYY - HH12:MI:SS')::text else 'No Asignado' end as creado
                    ,case when t.despachado is not null then to_char(t.despachado, 'DD/MM/YYYY - HH12:MI:SS')::text else 'No Asignado' end as alistamiento
                    ,case when t.entregado is not null then to_char(t.entregado, 'DD/MM/YYYY - HH12:MI:SS')::text else 'No Asignado' end as entregado
                        from pedido_pedido as p
                        inner join pedido_time as t on (t.pedido_id=p.id and p.num_pedido like ''||upper(nom_pedido)||'') inner join usuario_cliente as c on (c.id=p.cliente_id)  limit 1
    	) p2 into info;
        raise notice 'el valo res %',json_array_length(info);
        if json_array_length(info) = 0 then
            SELECT COALESCE(array_to_json(array_agg(row_to_json(p2))), '[]') from (
                select replace(cast(cast(p.cliente as json)::json->'nombre' as text)||' '||cast(cast(p.cliente as json)::json->'apellidos' as text),'"','') as cliente,
                        case when t.creado is not null then to_char(t.creado, 'DD/MM/YYYY - HH12:MI:SS')::text else 'No Asignado' end as creado
                        ,case when t.despachado is not null then to_char(t.despachado, 'DD/MM/YYYY - HH12:MI:SS')::text else 'No Asignado' end as alistamiento
                        ,case when t.entregado is not null then to_char(t.entregado, 'DD/MM/YYYY - HH12:MI:SS')::text else 'No Asignado' end as entregado
                            from pedido_pedidows as p
                            inner join pedido_timews as t on (p.id=t.pedido_id and p.num_pedido like ''||upper(nom_pedido)||'')  limit 1
            ) p2 into info;
            raise notice 'el valo res %',json_array_length(info);
            if json_array_length(info) > 0 then
                return '{"r":true,"lista":'||info||'}';
            end if;
            return '{"r":false}';
        end if;
        return '{"r":true,"lista":'||info||'}';
    end if;
    return '{"r":false}';
end;
$$language plpgsql;
select * from pedido_pedido as p inner join pedido_time as t on (t.pedido_id=p.id and p.num_pedido like '%OL_4%') inner join usuario_cliente as c on (c.id=p.cliente_id)  limit 1
select * from pedido_time
select c.first_name||' '||c.last_name as cliente,
        case when t.creado is not null then to_char(t.creado, 'DD/MM/YYYY - HH12:MI:SS')::text else 'No Asignado' end as creado
        ,case when t.despachado is not null then to_char(t.despachado, 'DD/MM/YYYY - HH12:MI:SS')::text else 'No Asignado' end as alistamiento
        ,case when t.entregado is not null then to_char(t.entregado, 'DD/MM/YYYY - HH12:MI:SS')::text else 'No Asignado' end as entregado from pedido_pedido as p inner join pedido_time as t on (t.pedido_id=p.id and p.num_pedido like '%OL_4%') inner join usuario_cliente as c on (c.id=p.cliente_id)  limit 1

select 'op_1543d434'~'([a-z]*[A-Z]*){0,2}_([0-9])+'
select to_char(current_timestamp, 'DD/MM/YYYY - HH12:MI:SS')

select * from pedido_pedidows as p
select replace(cast(cast(p.cliente as json)::json->'nombre' as text)||' '||cast(cast(p.cliente as json)::json->'apellidos' as text),'"','') as cliente,
        case when t.creado is not null then to_char(t.creado, 'DD/MM/YYYY - HH12:MI:SS')::text else 'No Asignado' end as creado
        ,case when t.despachado is not null then to_char(t.despachado, 'DD/MM/YYYY - HH12:MI:SS')::text else 'No Asignado' end as alistamiento
        ,case when t.entregado is not null then to_char(t.entregado, 'DD/MM/YYYY - HH12:MI:SS')::text else 'No Asignado' end as entregado from pedido_pedidows as p inner join pedido_timews as t on (p.id=t.pedido_id and p.num_pedido like '%'||upper('exws_3')||'%')  limit 1
select * from pedido_pedidows as p inner join pedido_timews as t on (p.id=t.pedido_id)
select * from pedido_pedidows as p inner join pedido_timews as t on (p.id=t.pedido_id)
select * from pedido_timews
select * from public.pedido_pedido where id=96
select * from pedido_time
