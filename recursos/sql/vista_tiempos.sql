-- View: pedidos_tiempos

-- DROP VIEW pedidos_tiempos;

CREATE OR REPLACE VIEW pedidos_tiempos AS 
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
    pf.entrega
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
                END AS entrega
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
                    (date_part('epoch'::text, t.entregado) - date_part('epoch'::text, t.despachado)) / 60::double precision AS entrega
                   FROM pedido_pedido p_1
                     JOIN auth_user m ON p_1.motorizado_id = m.id
                     JOIN auth_user a ON p_1.alistador_id = a.id
                     JOIN auth_user s ON p_1.supervisor_id = s.id
                     JOIN usuario_cliente c ON p_1.cliente_id = c.id
                     JOIN pedido_time t ON p_1.id = t.pedido_id
                     JOIN pedido_time ti ON ti.pedido_id = p_1.id
                  ORDER BY p_1.fecha_pedido DESC) p) pf;

ALTER TABLE pedidos_tiempos
  OWNER TO postgres;

select * from pedidos_tiempos