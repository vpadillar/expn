select * from public.pedido_pedido as p inner join public.pedido_configuraciontiempo as c on (p.empresa_id=c.empresa_id)
 where c.id = (select confi.id from public.pedido_configuraciontiempo as confi where confi.empresa_id=1 order by confi.id desc limit 1) and p.fecha_pedido
                between
                       case when extract(day from current_date) > c.primero and extract(day from current_date) < c.segundo then
                            cast(''||extract(year from current_date)||'-'||extract(month from current_date)||'-'||c.primero as date)
                               else
                            cast(''||extract(year from current_date)||'-'||extract(month from current_date)||'-'||c.segundo as date)
                        end
                and
                        case when extract(day from current_date) > c.primero and extract(day from current_date) < c.segundo then
                             cast(''||extract(year from current_date)||'-'||extract(month from current_date)||'-'||c.segundo as date)
                                else
                             cast(''||extract(year from current_date)||'-'||extract(month from current_date)+1||'-'||c.primero as date)end