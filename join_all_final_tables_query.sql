USE fig;

select
	mi.name
    ,mi.ingredients
    ,mi.allergens
    ,mi.picture_url
    ,r.name as restaurant_name
    ,fc.name as fig_category_name
from menu_item mi
left join restaurant r
	on r.restaurant_id = mi.restaurant_id
left join fig_category fc
	on fc.fig_category_id = mi.fig_category_id
;
