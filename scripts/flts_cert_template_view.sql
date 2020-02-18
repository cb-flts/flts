CREATE OR REPLACE VIEW cb_plot_vw_lht_certificate_template AS
SELECT cb_plot.id,
    cb_scheme.scheme_name AS scheme_name,
    cb_check_lht_land_rights_office.value AS land_rights_office,
    concat(cb_holder.holder_first_name, ' ', cb_holder.holder_surname) AS full_name,
    cb_holder.holder_identifier AS holder_id,
    cb_check_lht_marital_status.value AS marital_status,
    cb_plot.plot_number,
    cb_plot.upi,
    cb_plot.geom AS plot_geom,
    st_collect(cb_plot.geom) OVER (PARTITION BY cb_plot.scheme_id) AS scheme_plots,
    cb_check_lht_relevant_authority.value AS type_of_relevant_authority,
    cb_relevant_authority.name_of_relevant_authority,
    cb_check_lht_reg_division.value AS registration_division,
    cb_check_lht_region.value AS region,
    cb_scheme.area
   FROM cb_social_tenure_relationship
     JOIN cb_plot ON cb_social_tenure_relationship.plot_id = cb_plot.id
     JOIN cb_scheme ON cb_plot.scheme_id = cb_scheme.id
     JOIN cb_check_lht_land_rights_office ON cb_scheme.land_rights_office = cb_check_lht_land_rights_office.id
     JOIN cb_holder ON cb_social_tenure_relationship.holder_id = cb_holder.id
     JOIN cb_check_lht_marital_status ON cb_check_lht_marital_status.id = cb_holder.marital_status
     JOIN cb_check_lht_relevant_authority ON cb_check_lht_relevant_authority.id = cb_scheme.relevant_authority
     JOIN cb_relevant_authority ON cb_relevant_authority.id = cb_scheme.relevant_authority
     JOIN cb_check_lht_reg_division ON cb_check_lht_reg_division.id = cb_scheme.registration_division
     JOIN cb_check_lht_region ON cb_check_lht_region.id = cb_scheme.region;
