 /* A view for Holders report segregated by gender. */
 SELECT count(*) AS total_registered_holders,
    count(*) FILTER (WHERE ((cb_holder_vw_social_tenure_relationship.holder_marital_status)::text = 'Unmarried'::text)) AS unmarried_holders,
    count(*) FILTER (WHERE ((cb_holder_vw_social_tenure_relationship.holder_marital_status)::text = 'Married'::text)) AS married_holders
   FROM cb_holder_vw_social_tenure_relationship