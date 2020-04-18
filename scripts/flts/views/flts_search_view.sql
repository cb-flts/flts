  /* A view for the search module. */
CREATE OR REPLACE VIEW cb_vw_plot_search AS
 SELECT cb_plot.id,
    cb_plot.upi,
    cb_plot.geom,
    cb_plot.plot_number,
    cb_check_lht_plot_use.value AS plot_use,
    cb_plot.area,
    cb_scheme.scheme_name
   FROM ((cb_plot
     JOIN cb_check_lht_plot_use ON ((cb_check_lht_plot_use.id = cb_plot.use)))
     JOIN cb_scheme ON ((cb_scheme.id = cb_plot.scheme_id)))

CREATE OR REPLACE VIEW cb_vw_holder_search AS
    SELECT cb_holder.id,
        cb_holder.holder_first_name,
        cb_holder.holder_surname,
        cb_holder.holder_identifier
       FROM cb_holder

CREATE OR REPLACE VIEW cb_vw_scheme_search AS
    SELECT cb_scheme.id,
        cb_scheme.scheme_name,
        cb_check_lht_region.value AS region,
        cb_scheme.date_of_establishment,
        cb_scheme.date_of_approval
       FROM (cb_scheme
         JOIN cb_check_lht_region ON ((cb_check_lht_region.id = cb_scheme.region)))

CREATE OR REPLACE VIEW cb_vw_scheme_search AS
     SELECT cb_holder.id,
        cb_holder.juristic_person_name,
        cb_holder.juristic_person_number
       FROM cb_holder