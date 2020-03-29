/* A view for Holders report segregated by gender. */
CREATE OR REPLACE VIEW cb_holder_vw_lht_report_gender_template AS
 SELECT count(*) AS total_registered_holders,
    count(*) FILTER (WHERE ((cb_holder_vw_social_tenure_relationship.holder_holder_gender)::text = 'Female'::text)) AS female,
    count(*) FILTER (WHERE ((cb_holder_vw_social_tenure_relationship.holder_holder_gender)::text = 'Male'::text)) AS male
   FROM cb_holder_vw_social_tenure_relationship
