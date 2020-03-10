CREATE OR REPLACE VIEW cb_holder_vw_lht_report_gender_template AS
SELECT count(*) AS total_holders,
    count(*) FILTER (WHERE (cb_holder.holder_gender = 1)) AS female_occupants,
    count(*) FILTER (WHERE (cb_holder.holder_gender = 2)) AS male_occupants
FROM cb_holder