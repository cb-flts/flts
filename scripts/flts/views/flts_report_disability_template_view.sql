/* A view for Holders report segregated by disability status. */
CREATE OR REPLACE VIEW cb_holder_vw_lht_report_disability_template AS
SELECT count(*) AS total_registered_holders,
    count(*) FILTER (WHERE ((cb_holder_vw_social_tenure_relationship.holder_holder_disability_status)::text = 'Yes'::text)) AS holders_with_disability,
    count(*) FILTER (WHERE ((cb_holder_vw_social_tenure_relationship.holder_holder_disability_status)::text = 'No'::text)) AS holders_without_disability
   FROM cb_holder_vw_social_tenure_relationship
