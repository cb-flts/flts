--- LOG TABLES
-- ----------------------------
-- Scheme Log
-- ----------------------------

DROP TABLE IF EXISTS cb_scheme_log, cb_holder_log, cb_plot_log;

CREATE TABLE cb_scheme_log (
  "operation" varchar(1),
  "stamp" timestamp(6),
  "user_id" text,
  "id" int4,
  "scheme_name" varchar(50),
  "date_of_approval" date,
  "date_of_establishment" date,
  "relevant_authority" int4,
  "land_rights_office" int4,
  "region" int4,
  "title_deed_number" varchar(30),
  "registration_division" int4,
  "area" numeric(15,4),
  "doc_imposing_conditions_number" varchar(30),
  "constitution_ref_number" varchar(32),
  "no_of_plots" int4,
  "land_hold_plan_number" varchar(30),
  "scheme_number" varchar(32),
  "sg_number" varchar (32),
  "plot_status" int4,
  "scheme_description" varchar(200)
)
;

-- ----------------------------
-- Holder Log
-- ----------------------------

CREATE TABLE cb_holder_log (
  "operation" varchar(1),
  "stamp" timestamp(6),
  "user_id" text,
  "id" int4,
  "plot_number" int4,
  "transfer_contract_date" date,
  "plot_use" int4,
  "holder_first_name" varchar(50),
  "holder_surname" varchar(50),
  "holder_gender" int4,
  "holder_identifier" varchar(20),
  "holder_date_of_birth" date,
  "marital_status" int4,
  "nature_of_marriage" int4,
  "holder_disability_status" int4,
  "holder_income_level" int4,
  "holder_occupation" int4,
  "spouse_surname" varchar(50),
  "spouse_first_name" varchar(50),
  "spouse_gender" int4,
  "spouse_identifier" varchar(20),
  "spouse_date_of_birth" date,
  "other_dependants" int4,
  "juristic_person_name" varchar(50),
  "juristic_person_number" varchar(50)
)
;

-- ----------------------------
-- Plot Log
-- ----------------------------

CREATE TABLE cb_plot_log (
  "operation" varchar(1),
  "stamp" timestamp(6),
  "user_id" text,
  "id" int4,
  "upi" varchar(32),
  "geom" "public"."geometry",
  "use" int4,
  "plot_number" varchar(6),
  "area" numeric(18,6),
  "scheme_id" int4
)
;

--  TRIGGER FUNCTIONS
------ Scheme Log

CREATE OR REPLACE FUNCTION cb_scheme_log() RETURNS TRIGGER AS $cb_scheme_log$
    BEGIN
        --
        -- Create a row in lht_scheme_log to reflect the operation performed on cb_scheme,
        -- make use of the special variable TG_OP to work out the operation.
        --
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO cb_scheme_log SELECT 'D', now(), user, OLD.*;
            RETURN OLD;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO cb_scheme_log SELECT 'U', now(), user, NEW.*;
            RETURN NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO cb_scheme_log SELECT 'I', now(), user, NEW.*;
            RETURN NEW;
        END IF;
        RETURN NULL; -- result is ignored since this is an AFTER trigger
    END;
$cb_scheme_log$ LANGUAGE plpgsql;

------ Holder Log

CREATE OR REPLACE FUNCTION cb_holder_log() RETURNS TRIGGER AS $cb_holder_log$
    BEGIN
        --
        -- Create a row in lht_holder_log to reflect the operation performed on cb_holder,
        -- make use of the special variable TG_OP to work out the operation.
        --
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO cb_holder_log SELECT 'D', now(), user, OLD.*;
            RETURN OLD;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO cb_holder_log SELECT 'U', now(), user, NEW.*;
            RETURN NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO cb_holder_log SELECT 'I', now(), user, NEW.*;
            RETURN NEW;
        END IF;
        RETURN NULL; -- result is ignored since this is an AFTER trigger
    END;
$cb_holder_log$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION cb_plot_log() RETURNS TRIGGER AS $cb_plot_log$
    BEGIN
        --
        -- Create a row in lht_holder_log to reflect the operation performed on cb_holder,
        -- make use of the special variable TG_OP to work out the operation.
        --
        IF (TG_OP = 'DELETE') THEN
            INSERT INTO cb_plot_log SELECT 'D', now(), user, OLD.*;
            RETURN OLD;
        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO cb_plot_log SELECT 'U', now(), user, NEW.*;
            RETURN NEW;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO cb_plot_log SELECT 'I', now(), user, NEW.*;
            RETURN NEW;
        END IF;
        RETURN NULL; -- result is ignored since this is an AFTER trigger
    END;
$cb_plot_log$ LANGUAGE plpgsql;

-- CREATE OR REPLACE FUNCTION cb_plot_num_drop_zeros() RETURNS TRIGGER AS $cb_plot_num_drop_zeros$
--     BEGIN
--         NEW.plot_number=(NEW.plot_number::INTEGER)::TEXT;
--         RETURN NEW;
--     END;
-- $cb_plot_num_drop_zeros$ LANGUAGE plpgsql;

------ Timestamp

CREATE OR REPLACE FUNCTION insert_timestamp() RETURNS TRIGGER AS $insert_timestamp$
    BEGIN
        NEW.timestamp = NOW();
				RETURN NEW;
    END;

$insert_timestamp$ LANGUAGE plpgsql;

--- TRIGGERS

CREATE TRIGGER cb_scheme_log
AFTER INSERT OR UPDATE OR DELETE ON cb_scheme
    FOR EACH ROW EXECUTE PROCEDURE cb_scheme_log();

CREATE TRIGGER cb_holder_log
AFTER INSERT OR UPDATE OR DELETE ON cb_holder
    FOR EACH ROW EXECUTE PROCEDURE cb_holder_log();

-- CREATE TRIGGER cb_plot_num_drop_zeros
-- BEFORE INSERT OR UPDATE ON cb_plot
--     FOR EACH ROW EXECUTE PROCEDURE cb_plot_num_drop_zeros();

CREATE TRIGGER cb_plot_log
AFTER INSERT ON cb_plot
    FOR EACH ROW EXECUTE PROCEDURE cb_plot_log();

CREATE TRIGGER comment_timestamp
BEFORE INSERT OR UPDATE ON cb_comment
    FOR EACH ROW EXECUTE PROCEDURE insert_timestamp();

CREATE TRIGGER insert_workflow_timestamp
BEFORE INSERT OR UPDATE ON cb_scheme_workflow
    FOR EACH ROW EXECUTE PROCEDURE insert_timestamp();

---- TODO Add exception handling
