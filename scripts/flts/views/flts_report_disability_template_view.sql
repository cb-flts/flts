/* A view for Holders report segregated by disability status. */

CREATE OR REPLACE VIEW cb_holder_vw_lht_report_disability_template AS
SELECT count(*) AS total_holders,
    count(*) FILTER (WHERE (cb_holder.holder_disability_status = 1)) AS disabled,
    count(*) FILTER (WHERE (cb_holder.holder_disability_status = 2)) AS not_disabled
FROM cb_holder
