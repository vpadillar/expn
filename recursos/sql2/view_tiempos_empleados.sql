-- View: pedidos_tiempos

-- DROP VIEW pedidos_tiempos;
select * from 
CREATE OR REPLACE VIEW pedidos_tiempos_actualizada AS 
 SELECT pf.nump,
    pf.cliente,
    pf.supervisor,
    pf.alistador,
    pf.motori,
    pf.direccion,
    pf.total,
    pf.cliente_id,
    pf.supervisor_id,
    pf.alistador_id,
    pf.motorizado_id,
    pf.empresa_id,
    pf.fecha,
    pf.alistar,
    pf.despacho,
    pf.entrega,
    pf.estado,
    pf.tienda,
    pf.ciudad
   FROM ( SELECT p.nump,
            p.cliente,
            p.supervisor,
            p.alistador,
            p.motori,
            p.direccion,
            p.total,
            p.cliente_id,
            p.supervisor_id,
            p.alistador_id,
            p.motorizado_id,
            p.empresa_id,
            p.fecha,
                CASE
                    WHEN p.alistamiento IS NOT NULL THEN round(p.alistamiento::numeric, 2)::text
                    ELSE 'No asignado'::text
                END AS alistar,
                CASE
                    WHEN p.despacho IS NOT NULL THEN round(p.despacho::numeric, 2)::text
                    ELSE 'No asignado'::text
                END AS despacho,
                CASE
                    WHEN p.entrega IS NOT NULL THEN round(p.entrega::numeric, 2)::text
                    ELSE 'No asignado'::text
                END AS entrega,
                p.empresa_id as empresa,
                p.ciudad,
                p.tienda,
                p.estado
           FROM ( SELECT p_1.id,
	    p_1.num_pedido AS nump,
	    (c.first_name::text || ' '::text) || c.last_name::text AS cliente,
	    (s.first_name::text || ' '::text) || s.last_name::text AS supervisor,
	    c.direccion,
	    p_1.cliente_id,
	    p_1.alistador_id,
	    p_1.motorizado_id,
	    p_1.supervisor_id,
	    (a.first_name::text || ' '::text) || a.last_name::text AS alistador,
	    (m.first_name::text || ' '::text) || m.last_name::text AS motori,
	    p_1.empresa_id,
	    p_1.fecha_pedido AS fecha,
		CASE
		    WHEN p_1.total IS NOT NULL THEN p_1.total
		    ELSE 0::numeric
		END::text AS total,
	    (date_part('epoch'::text, t.confirmado) - date_part('epoch'::text, t.creado)) / 60::double precision AS alistamiento,
	    (date_part('epoch'::text, t.despachado) - date_part('epoch'::text, t.confirmado)) / 60::double precision AS despacho,
	    (date_part('epoch'::text, t.entregado) - date_part('epoch'::text, t.despachado)) / 60::double precision AS entrega,
	    p_1.tienda_id as tienda,
	    tiend.ciudad_id as ciudad,
	    p_1.entregado as estado
	   FROM pedido_pedido p_1
	     JOIN auth_user m ON p_1.motorizado_id = m.id
	     JOIN auth_user a ON p_1.alistador_id = a.id
	     JOIN auth_user s ON p_1.supervisor_id = s.id
	     JOIN usuario_cliente c ON p_1.cliente_id = c.id
	     JOIN pedido_time t ON p_1.id = t.pedido_id
	     JOIN pedido_time ti ON ti.pedido_id = p_1.id
	     join usuario_tienda as tiend on (tiend.id=p_1.tienda_id)
	   union
	    select pws.id,case when pws.num_pedido is null or length(pws.num_pedido) =0 then 'PdWs' else pws.num_pedido end as nump,
		cast(pws.cliente as json)::json->>'nombre'||' '||(cast(pws.cliente as json)::json->>'apellidos') as cliente,
		'Super_Ws' as supervisor, 
		cast(pws.cliente as json)::json->>'direccion',
		0 as cliente_id,
		0 as alistador_id,
		case when pws.motorizado_id is not null then pws.motorizado_id 	else 0 end as motorizado_id,
		0 as supervisor_id,
		'Alistador Pws'::text as alistador,
		m.first_name||' '||m.last_name as motori,
		tiend.empresa_id,
		pws.fecha_pedido as fecha,
		CASE
		    WHEN pws.total IS NOT NULL THEN pws.total
		    ELSE 0::numeric
		END::text AS total,
		(date_part('epoch'::text, t.confirmado) - date_part('epoch'::text,  t.creado)) / 60::double precision AS alistamiento,
		(date_part('epoch'::text, t.despachado) - date_part('epoch'::text, t.confirmado)) / 60::double precision AS despacho,
		(date_part('epoch'::text, t.entregado) - date_part('epoch'::text, t.despachado)) / 60::double precision AS entrega,
		pws.tienda_id as tienda,
		tiend.ciudad_id as ciudad,
		pws.entregado as estado
		from pedido_pedidows as pws 
		inner join auth_user as m ON (pws.motorizado_id = m.id)
		inner join usuario_tienda as tiend on (tiend.id=pws.tienda_id)
		inner join pedido_timews as t on (pws.id=t.pedido_id)
	) p) pf ORDER BY pf.fecha;

ALTER TABLE pedidos_tiempos
  OWNER TO postgres;


select * from usuario_tienda
select * from pedido_pedidows

SELECT p_1.id,
    p_1.num_pedido AS nump,
    (c.first_name::text || ' '::text) || c.last_name::text AS cliente,
    (s.first_name::text || ' '::text) || s.last_name::text AS supervisor,
    c.direccion,
    p_1.cliente_id,
    p_1.alistador_id,
    p_1.motorizado_id,
    p_1.supervisor_id,
    (a.first_name::text || ' '::text) || a.last_name::text AS alistador,
    (m.first_name::text || ' '::text) || m.last_name::text AS motori,
    p_1.empresa_id,
    p_1.fecha_pedido AS fecha,
	CASE
	    WHEN p_1.total IS NOT NULL THEN p_1.total
	    ELSE 0::numeric
	END::text AS total,
    (date_part('epoch'::text, t.confirmado) - date_part('epoch'::text, t.creado)) / 60::double precision AS alistamiento,
    (date_part('epoch'::text, t.despachado) - date_part('epoch'::text, t.confirmado)) / 60::double precision AS despacho,
    (date_part('epoch'::text, t.entregado) - date_part('epoch'::text, t.despachado)) / 60::double precision AS entrega,
    p_1.tienda_id as tienda,
    tiend.ciudad_id as ciudad,
    p_1.entregado as estado
   FROM pedido_pedido p_1
     JOIN auth_user m ON p_1.motorizado_id = m.id
     JOIN auth_user a ON p_1.alistador_id = a.id
     JOIN auth_user s ON p_1.supervisor_id = s.id
     JOIN usuario_cliente c ON p_1.cliente_id = c.id
     JOIN pedido_time t ON p_1.id = t.pedido_id
     JOIN pedido_time ti ON ti.pedido_id = p_1.id
     join usuario_tienda as tiend on (tiend.id=p_1.tienda_id)
union
select pws.id,case when pws.num_pedido is null or length(pws.num_pedido) =0 then 'PdWs' else pws.num_pedido end as nump,
	cast(pws.cliente as json)::json->>'nombre'||' '||(cast(pws.cliente as json)::json->>'apellidos') as cliente,
	'Super_Ws' as supervisor, 
	cast(pws.cliente as json)::json->>'direccion',
	0 as cliente_id,
	0 as alistador_id,
	case when pws.motorizado_id is not null then pws.motorizado_id 	else 0 end as motorizado_id,
	0 as supervisor_id,
	'Alistador Pws'::text as alistador,
	m.first_name||' '||m.last_name as motori,
	tiend.empresa_id,
	pws.fecha_pedido as fecha,
	CASE
	    WHEN pws.total IS NOT NULL THEN pws.total
	    ELSE 0::numeric
	END::text AS total,
	(date_part('epoch'::text, t.confirmado) - date_part('epoch'::text,  t.creado)) / 60::double precision AS alistamiento,
	(date_part('epoch'::text, t.despachado) - date_part('epoch'::text, t.confirmado)) / 60::double precision AS despacho,
	(date_part('epoch'::text, t.entregado) - date_part('epoch'::text, t.despachado)) / 60::double precision AS entrega,
	pws.tienda_id as tienda,
	tiend.ciudad_id as ciudad,
	pws.entregado as estado
	from pedido_pedidows as pws 
	inner join auth_user as m ON (pws.motorizado_id = m.id)
	inner join usuario_tienda as tiend on (tiend.id=pws.tienda_id)
	inner join pedido_timews as t on (pws.id=t.pedido_id)



select * from pedido_pedidows where motorizado_id is null
update pedido_pedidows set cliente = replace(cliente,'dirreccion','direccion')
select pws.id,case when pws.num_pedido is null or length(pws.num_pedido) =0 then 'PdWs' else pws.num_pedido end as nump,
	cast(pws.cliente as json)::json->>'nombre'||' '||(cast(pws.cliente as json)::json->>'apellidos') as cliente,
	case when pws.supervisor_id is null then 0 else pws.supervisor_id end as supervisor, 
	cast(pws.cliente as json)::json->>'direccion',
	0 as cliente_id,
	0 as alistador_id,
	case when pws.motorizado_id is not null then pws.motorizado_id 	else 0 end as motorizado_id,
	0 as supervisor_id,
	'Alistador Pws'::text as alistador,
	m.first_name||' '||m.last_name as motori,
	tiend.empresa_id,
	pws.fecha_pedido as fecha,
	CASE
	    WHEN pws.total IS NOT NULL THEN pws.total
	    ELSE 0::numeric
	END::text AS total,
	(date_part('epoch'::text, t.confirmado) - date_part('epoch'::text,  t.creado)) / 60::double precision AS alistamiento,
	(date_part('epoch'::text, t.despachado) - date_part('epoch'::text, t.confirmado)) / 60::double precision AS despacho,
	(date_part('epoch'::text, t.entregado) - date_part('epoch'::text, t.despachado)) / 60::double precision AS entrega,
	pws.tienda_id as tienda,
	tiend.ciudad_id as ciudad,
	pws.entregado as estado
	from pedido_pedidows as pws 
	inner join auth_user as m ON (pws.motorizado_id = m.id)
	inner join usuario_tienda as tiend on (tiend.id=pws.tienda_id)
	inner join pedido_timews as t on (pws.id=t.pedido_id)


select * from pedido_timews

select * from pedido_pedido
select * from usuario_tienda

select aceptar_pw_service(343,'778d2d83f54a9ccb')
select * from pedido_pedidows where id=342

select date_part('epoch'::text, alistado) from pedido_timews