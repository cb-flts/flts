-- This creates the view for the certificate of Land Hold Title(LHT)
CREATE OR REPLACE VIEW cb_holder_vw_lht_report_template AS
    SELECT cb_plot.id,
        concat(cb_scheme.scheme_name, ' Scheme') AS scheme_name,
        cb_scheme.scheme_number,
        cb_scheme.land_hold_plan_number,
        concat('I, the Land Rights Registrar at ', cb_check_lht_land_rights_office.value, ', hereby certify that') AS land_rights_office_text,
        concat(cb_holder.holder_first_name, ' ', cb_holder.holder_surname) AS full_name,
        concat('Identity Number ', cb_holder.holder_identifier) AS holder_id,
        cb_check_lht_marital_status.value AS marital_status,
        concat('Plot No: ', (cb_plot.plot_number)::integer) AS plot_number,
        cb_plot.upi,
        cb_plot.geom AS plot_geom,
        concat(rtrim((cb_check_lht_relevant_authority.value)::text, 'Council'::text), 'of ', cb_relevant_authority.name_of_relevant_authority) AS authority,
        concat(rtrim((cb_check_lht_relevant_authority.value)::text, 'Council'::text), 'of ', cb_relevant_authority.name_of_relevant_authority, ', ', cb_check_lht_region.value, ' Region') AS ra_region,
        concat('Registration Division ', cb_check_lht_reg_division.value) AS reg_division,
        concat(cb_check_lht_region.value, ' Region') AS region,
        concat(flts_plot_area_to_text(cb_plot.area), cb_scheme.land_hold_plan_number, ';') AS area_in_words,
        concat('No. ', cb_scheme.land_hold_plan_number) AS land_hold_plan_no_text,
        concat('Plot No: ', (cb_plot.plot_number)::integer, ', ', cb_scheme.scheme_name, ' Scheme') AS plot_scheme_text,
        flts_get_spouse_name(cb_holder.*) AS spouse_name,
        flts_append_and_to_spouse_name(cb_holder.*) AS append_and,
        flts_get_spouse_document_identifier(cb_holder.*) AS spouse_document_identifier,
        flts_get_holder_nature_of_marriage(cb_holder.*) AS nature_of_marriage,
        flts_get_scheme_imposing_condition(cb_scheme.*) AS imposing_condition_text,
        flts_gen_cert_number() AS certificate_number,
        concat('Cerificate No. ', flts_gen_cert_number()) AS certificate_number_text
       FROM (((((((((cb_social_tenure_relationship
         JOIN cb_plot ON ((cb_social_tenure_relationship.plot_id = cb_plot.id)))
         JOIN cb_scheme ON ((cb_plot.scheme_id = cb_scheme.id)))
         JOIN cb_check_lht_land_rights_office ON ((cb_scheme.land_rights_office = cb_check_lht_land_rights_office.id)))
         JOIN cb_holder ON ((cb_social_tenure_relationship.holder_id = cb_holder.id)))
         JOIN cb_check_lht_marital_status ON ((cb_check_lht_marital_status.id = cb_holder.marital_status)))
         JOIN cb_relevant_authority ON (((cb_relevant_authority.au_code)::text = 'OSHKTI'::text)))
         JOIN cb_check_lht_relevant_authority ON ((cb_check_lht_relevant_authority.id = cb_scheme.relevant_authority)))
         JOIN cb_check_lht_reg_division ON ((cb_check_lht_reg_division.id = cb_scheme.registration_division)))
         JOIN cb_check_lht_region ON ((cb_check_lht_region.id = cb_scheme.region)))