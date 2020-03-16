--- Appends and to spouse name where spouse name exists
CREATE OR REPLACE FUNCTION "public"."flts_append_and_to_spouse_name"("holder_row" "public"."cb_holder")
  RETURNS "pg_catalog"."text" AS $BODY$BEGIN
	IF holder_row.marital_status = 4 THEN
		RETURN 'and';
	ELSE
		RETURN '';
	END IF;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

--- Generates a new certificate number when a certificate is created
CREATE OR REPLACE FUNCTION "public"."flts_gen_cert_number"()
  RETURNS "pg_catalog"."text" AS $BODY$DECLARE
cert_num TEXT;
current_year TEXT;
current_num INTEGER := 1;
BEGIN
	SELECT MAX(certificate_number) INTO cert_num FROM cb_certificate;
	current_year := date_part('year', now())::TEXT;
	IF cert_num IS NOT NULL THEN
		current_num := split_part(split_part(cert_num, '/', 1), 'H', 2)::INTEGER;
		current_num := current_num + 1;
	END IF;
	RETURN 'LH'|| lpad(current_num::TEXT, 5, '0') || '/' || current_year;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

--- Checks the nature of marriage if holder is married
CREATE OR REPLACE FUNCTION "public"."flts_get_holder_nature_of_marriage"("holder_row" "public"."cb_holder")
  RETURNS "pg_catalog"."text" AS $BODY$DECLARE
	nature_of_marriage text;
BEGIN
	IF holder_row.marital_status = 4 THEN
		SELECT value INTO nature_of_marriage FROM cb_check_lht_nature_of_marriage WHERE id = holder_row.nature_of_marriage;
		RETURN 'who are married, ' || lower(nature_of_marriage);
	ELSE
		RETURN '';
	END IF;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

--- Generates a string text if the scheme has imposing conditions
CREATE OR REPLACE FUNCTION "public"."flts_get_scheme_imposing_condition"("scheme_row" "public"."cb_scheme")
  RETURNS "pg_catalog"."text" AS $BODY$DECLARE
	doc_row cb_scheme_supporting_document%ROWTYPE;
	condition_txt TEXT := 'Subject to the conditions imposed by Municipality of Windhoek in terms of section 13(6) of the Flexible Land Tenure Act, 2012 (Act No. 4 of 2012) registered in the Land Rights Office, Reference No: FK.';
BEGIN
	SELECT * INTO doc_row FROM cb_scheme_supporting_document WHERE (cb_scheme_supporting_document.scheme_id = scheme_row.id AND cb_scheme_supporting_document.document_type = 7);
	IF doc_row IS NULL THEN
		RETURN '';
	ELSE
		RETURN condition_txt || scheme_row.scheme_number;
	END IF;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

--- Gets the ID number of the spouse if the holder is married
CREATE OR REPLACE FUNCTION "public"."flts_get_spouse_document_identifier"("holder_row" "public"."cb_holder")
  RETURNS "pg_catalog"."text" AS $BODY$BEGIN
	IF holder_row.marital_status = 4 THEN
		RETURN 'Identity Number ' || holder_row.spouse_identifier;
	ELSE
		RETURN '';
	END IF;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

--- Gets the spouse name if the holder is married
CREATE OR REPLACE FUNCTION "public"."flts_get_spouse_name"("holder_row" "public"."cb_holder")
  RETURNS "pg_catalog"."text" AS $BODY$BEGIN
	IF holder_row.marital_status = 4 THEN
		RETURN holder_row.spouse_first_name || ' ' || holder_row.spouse_surname;
	ELSE
		RETURN '';
	END IF;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

--- Converts area value to words
CREATE OR REPLACE FUNCTION "public"."flts_integer_to_text"(int4)
  RETURNS "pg_catalog"."text" AS $BODY$SELECT CASE WHEN $1<1 THEN NULL
              WHEN $1=1 THEN 'One'
              WHEN $1=2 THEN 'Two'
              WHEN $1=3 THEN 'Three'
              WHEN $1=4 THEN 'Four'
              WHEN $1=5 THEN 'Five'
              WHEN $1=6 THEN 'Six'
              WHEN $1=7 THEN 'Seven'
              WHEN $1=8 THEN 'Eight'
              WHEN $1=9 THEN 'Nine'
              WHEN $1=10 THEN 'Ten'
              WHEN $1=11 THEN 'Eleven'
              WHEN $1=12 THEN 'Twelve'
              WHEN $1=13 THEN 'Thirteen'
              WHEN $1=14 THEN 'Fourteen'
              WHEN $1=15 THEN 'Fifteen'
              WHEN $1=16 THEN 'Sixteen'
              WHEN $1=17 THEN 'Seventeen'
              WHEN $1=18 THEN 'Eighteen'
              WHEN $1=19 THEN 'Nineteen'
              WHEN $1<100 THEN CASE
                 WHEN $1/10=2 THEN 'Twenty' || COALESCE(' ' || flts_integer_to_text($1%10), '')
                 WHEN $1/10=3 THEN 'Thirty' || COALESCE(' ' || flts_integer_to_text($1%10), '')
                 WHEN $1/10=4 THEN 'Fourty' || COALESCE(' ' || flts_integer_to_text($1%10), '')
                 WHEN $1/10=5 THEN 'Fifty' || COALESCE(' ' || flts_integer_to_text($1%10), '')
                 WHEN $1/10=6 THEN 'Sixty' || COALESCE(' ' || flts_integer_to_text($1%10), '')
                 WHEN $1/10=7 THEN 'Seventy' || COALESCE(' ' || flts_integer_to_text($1%10), '')
                 WHEN $1/10=8 THEN 'Eighty' || COALESCE(' ' || flts_integer_to_text($1%10), '')
                 WHEN $1/10=9 THEN 'Ninety' || COALESCE(' ' || flts_integer_to_text($1%10), '')
              END
              WHEN $1<1000
                 THEN flts_integer_to_text($1/100) || ' Hundred' ||
                      COALESCE(' and ' || flts_integer_to_text($1%100), '')
              WHEN $1<1000000
                 THEN flts_integer_to_text($1/1000) || ' Thousand' ||
                      CASE WHEN $1%1000 < 100
                         THEN COALESCE(' and ' || flts_integer_to_text($1%1000), '')
                         ELSE COALESCE(' ' || flts_integer_to_text($1%1000), '')
                      END
              WHEN $1<1000000000
                 THEN flts_integer_to_text($1/1000000) || ' Million' ||
                      CASE WHEN $1%1000000 < 100
                         THEN COALESCE(' and ' || flts_integer_to_text($1%1000000), '')
                         ELSE COALESCE(' ' || flts_integer_to_text($1%1000000), '')
                      END
              ELSE NULL
         END$BODY$
  LANGUAGE sql IMMUTABLE STRICT
  COST 100;

--- Appends text to the area value in text
CREATE OR REPLACE FUNCTION "public"."flts_plot_area_to_text"("area" numeric)
  RETURNS "pg_catalog"."text" AS $BODY$DECLARE
	units VARCHAR(15);
	plot_area_txt TEXT;
	rounded_area INTEGER;
	measurement_txt TEXT := ', as shown and more fully described on the Land Hold Plan No. ';
BEGIN
	IF area < 10000 THEN
		rounded_area := round(area)::INTEGER;
		units := 'Square Meters';
	ELSE
		rounded_area := round(area/10000)::INTEGER;
		units := 'Hectares';
	END IF;

	RETURN rounded_area::TEXT || ' (' || flts_integer_to_text(rounded_area) || ') ' || units || measurement_txt;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;


