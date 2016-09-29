CREATE OR REPLACE VIEW pedidos_motorizados as 
select
	pedido.id,
	ptime.creado,
	ptime.confirmado,
	ptime.despachado,
	ptime.entregado,
	pedido.motorizado_id
from public.pedido_pedido as pedido
join public.pedido_time as ptime on pedido.id = ptime.pedido_id

where motorizado_id is not null

union

select
	pedido.id,
	ptime.creado,
	ptime.confirmado,
	ptime.despachado,
	ptime.entregado,
	pedido.motorizado_id
from public.pedido_pedidows as pedido
join public.pedido_timews as ptime on pedido.id = ptime.pedido_id

where pedido.motorizado_id is not null;


select * from pedidos_motorizados;
