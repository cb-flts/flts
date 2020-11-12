/***************************************************************************
Name                 : Flexible Land Tenure System
Description          : Tables populating scripts
Date                 : 30-04-2020
copyright            : (C) 2020 by UN-Habitat and implementing partners.
                       See the accompanying file CONTRIBUTORS.txt in the root
email                : stdm@unhabitat.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/


----------------Populate relevant authorities------------------------

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Gobabis', 'GOBBIS', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
	WHERE ra.value = 'Municipality Council' AND region.value = 'Omaheke';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Grootfontein', 'GRTFIN', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Municipality Council' AND region.value = 'Otjozondjupa';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Henties Bay', 'HENTAY', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Municipality Council' AND region.value = 'Erongo';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Keetmanshoop', 'KETMOP', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Municipality Council' AND region.value = 'Karas';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Mariental', 'MARNAL', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Municipality Council' AND region.value = 'Hardap';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Okahandja', 'OKHNJA', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Municipality Council' AND region.value = 'Otjozondjupa';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Omaruru', 'OMARRU', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Municipality Council' AND region.value = 'Erongo';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Otjiwarongo', 'OTJWGO', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Municipality Council' AND region.value = 'Otjozondjupa';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Outjo', 'OUTJOX', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Municipality Council' AND region.value = 'Kunene';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Swakopmund', 'SWKPND', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Municipality Council' AND region.value = 'Erongo';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Tsumeb', 'TSUMEB', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Municipality Council' AND region.value = 'Oshikoto';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Walvis Bay', 'WALVAY', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Municipality Council' AND region.value = 'Erongo';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Windhoek', 'WINDEK', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Municipality Council' AND region.value = 'Khomas';

--TOWN COUNCIL:

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Arandis', 'ARNDIS', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Erongo';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Aranos', 'ARANOS', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Hardap';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Eenhana', 'EENHNA', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Ohangwena';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Helao Nafidi', 'HELNDI', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Ohangwena';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Karasburg', 'KARSRG', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Karas';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Karibib', 'KARBIB', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Erongo';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Katima Mulilo', 'KATMLO', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Zambezi';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Khorixas', 'KHRXAS', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Kunene';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Luderitz', 'LUDRTZ', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Karas';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Nkurenkuru', 'NKRNRU', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Kavango West';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Okahao', 'OKAHAO', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Omusati';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Okakarara', 'OKKRRA', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Otjozondjupa';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Omuthiya', 'OMTHYA', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Oshikoto';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Ondangwa', 'ONDNWA', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Oshana';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Ongwediva', 'ONGWVA', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Oshana';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Oniipa', 'ONIIPA', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Oshikoto';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Opuwo', 'OPUWOX', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Kunene';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Oranjemund', 'ORNJND', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Karas';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Oshakati', 'OSHKTI', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Oshana';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Oshikuku', 'OSHKKU', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Omusati';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Otavi', 'OTAVIX', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Otjozondjupa';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Outapi', 'OUTAPI', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Omusati';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Rehoboth', 'REHBTH', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Hardap';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Ruacana', 'RUACNA', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Omusati';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Rundu', 'RUNDUX', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Kavango East';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Usakos', 'USAKOS', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Town Council' AND region.value = 'Erongo';

--VILLAGE COUNCIL:

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Aroab', 'AROABX', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Village Council' AND region.value = 'Karas';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Berseba', 'BERSBA', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Village Council' AND region.value = 'Karas';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Bethanie', 'BETHIE', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Village Council' AND region.value = 'Karas';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Bukalo', 'BUKALO', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Village Council' AND region.value = 'Zambezi';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Divundu', 'DIVNDU', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Village Council' AND region.value = 'Kavango East';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Gibeon', 'GIBEON', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Village Council' AND region.value = 'Hardap';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Gochas', 'GOCHAS', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Village Council' AND region.value = 'Hardap';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Kalkrand', 'KALKND', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Village Council' AND region.value = 'Hardap';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Kamanjab', 'KAMNAB', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Village Council' AND region.value = 'Kunene';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Koës', 'KOESXX', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Village Council' AND region.value = 'Karas';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Leonardville', 'LENRLE', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Village Council' AND region.value = 'Omaheke';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Luhonono', 'LUHNNO', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Village Council' AND region.value = 'Zambezi';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Maltahöhe', 'MALTHE', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Village Council' AND region.value = 'Hardap';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Okongo', 'OKONGO', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Village Council' AND region.value = 'Ohangwena';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Otjinene', 'OTJNNE', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Village Council' AND region.value = 'Omaheke';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Stampriet', 'STMPET', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Village Council' AND region.value = 'Hardap';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Tsandi', 'TSANDI', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Village Council' AND region.value = 'Omusati';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Tses', 'TSESXX', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Village Council' AND region.value = 'Karas';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Witvlei', 'WITVEI', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Village Council' AND region.value = 'Omaheke';

--REGIONAL COUNCIL:

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Erongo', 'ERONGO', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Regional Council' AND region.value = 'Erongo';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Hardap', 'HARDAP', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Regional Council' AND region.value = 'Hardap';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Karas', 'KARASX', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Regional Council' AND region.value = 'Karas';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Kavango East', 'KAVEST', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Regional Council' AND region.value = 'Kavango East';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Kavango West', 'KAVWST', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Regional Council' AND region.value = 'Kavango West';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Khomas', 'KHOMAS', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Regional Council' AND region.value = 'Khomas';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Kunene', 'KUNENE', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Regional Council' AND region.value = 'Kunene';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Ohangwena', 'OHNGNA', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Regional Council' AND region.value = 'Ohangwena';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Omaheke', 'OMAHKE', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Regional Council' AND region.value = 'Omaheke';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Omusati', 'OMUSTI', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Regional Council' AND region.value = 'Omusati';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Oshana', 'OSHANA', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Regional Council' AND region.value = 'Oshana';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Oshikoto', 'OSHKTO', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Regional Council' AND region.value = 'Oshikoto';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Otjozondjupa', 'OTZNPA', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Regional Council' AND region.value = 'Otjozondjupa';

INSERT INTO cb_relevant_authority (name_of_relevant_authority, au_code, type_of_relevant_authority, region)
    SELECT 'Zambezi', 'ZAMBZI', ra.id, region.id
    FROM cb_check_lht_relevant_authority ra, cb_check_lht_region region
    WHERE ra.value = 'Regional Council' AND region.value = 'Zambezi';

----------------Populate registration divisions----------------------

-- Municipality

INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'GOBBIS' AND regdiv.value = 'L';

INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'GRTFIN' AND regdiv.value = 'B';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'HENTAY' AND regdiv.value = 'G';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'KETMOP' AND regdiv.value = 'T';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'MARNAL' AND regdiv.value = 'R';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OKHNJA' AND regdiv.value = 'J';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OMARRU' AND regdiv.value = 'C';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OTJWGO' AND regdiv.value = 'D';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OUTJOX' AND regdiv.value = 'A';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'SWKPND' AND regdiv.value = 'G';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'TSUMEB' AND regdiv.value = 'B';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'WALVAY' AND regdiv.value = 'F';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'WINDEK' AND regdiv.value = 'K';

	-- Town Council

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'ARNDIS' AND regdiv.value = 'G';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'ARANOS' AND regdiv.value = 'R';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'EENHNA' AND regdiv.value = 'A';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'HELNDI' AND regdiv.value = 'A';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'KARSRG' AND regdiv.value = 'V';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'KARBIB' AND regdiv.value = 'H';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'KATMLO' AND regdiv.value = 'B';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'KHRXAS' AND regdiv.value = 'A';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'LUDRTZ' AND regdiv.value = 'N';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'NKRNRU' AND regdiv.value = 'B';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OKAHAO' AND regdiv.value = 'A';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OKKRRA' AND regdiv.value = 'D';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OMTHYA' AND regdiv.value = 'A';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'ONDNWA' AND regdiv.value = 'A';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'ONGWVA' AND regdiv.value = 'A';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'ONIIPA' AND regdiv.value = 'A';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OPUWOX' AND regdiv.value = 'A';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'ORNJND' AND regdiv.value = 'N';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OSHKTI' AND regdiv.value = 'A';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OSHKKU' AND regdiv.value = 'A';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OTAVIX' AND regdiv.value = 'B';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OUTAPI' AND regdiv.value = 'A';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'REHBTH' AND regdiv.value = 'M';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'RUACNA' AND regdiv.value = 'A';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'RUNDUX' AND regdiv.value = 'B';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'USAKOS' AND regdiv.value = 'H';

-- Village Council

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'AROABX' AND regdiv.value = 'T';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'BERSBA' AND regdiv.value = 'T';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'BUKALO' AND regdiv.value = 'B';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'BETHIE' AND regdiv.value = 'S';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'DIVNDU' AND regdiv.value = 'B';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'GIBEON' AND regdiv.value = 'R';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'GOCHAS' AND regdiv.value = 'R';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'KALKND' AND regdiv.value = 'M';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'KAMNAB' AND regdiv.value = 'A';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'KOESXX' AND regdiv.value = 'T';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'LENRLE' AND regdiv.value = 'L';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'LUHNNO' AND regdiv.value = 'L';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'MALTHE' AND regdiv.value = 'P';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OKONGO' AND regdiv.value = 'A';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OTJNNE' AND regdiv.value = 'L';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'STMPET' AND regdiv.value = 'R';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'TSANDI' AND regdiv.value = 'A';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'TSESXX' AND regdiv.value = 'T';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'MWITVEI' AND regdiv.value = 'L';

	-- Regional Council

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'ERONGO' AND regdiv.value = 'C';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'ERONGO' AND regdiv.value = 'F';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'ERONGO' AND regdiv.value = 'G';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'ERONGO' AND regdiv.value = 'H';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'ERONGO' AND regdiv.value = 'K';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'HARDAP' AND regdiv.value = 'L';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'HARDAP' AND regdiv.value = 'M';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'HARDAP' AND regdiv.value = 'N';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'HARDAP' AND regdiv.value = 'P';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'HARDAP' AND regdiv.value = 'R';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'HARDAP' AND regdiv.value = 'S';

INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'HARDAP' AND regdiv.value = 'T';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'KARASX' AND regdiv.value = 'N';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'KARASX' AND regdiv.value = 'S';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'KARASX' AND regdiv.value = 'T';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'KARASX' AND regdiv.value = 'V';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'KAVEST' AND regdiv.value = 'B';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'KAVWST' AND regdiv.value = 'B';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'KHOMAS' AND regdiv.value = 'G';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'KHOMAS' AND regdiv.value = 'J';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'KHOMAS' AND regdiv.value = 'K';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'KHOMAS' AND regdiv.value = 'L';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'KHOMAS' AND regdiv.value = 'M';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'KHOMAS' AND regdiv.value = 'N';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'KUNENE' AND regdiv.value = 'A';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OHNGNA' AND regdiv.value = 'A';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OHNGNA' AND regdiv.value = 'B';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OMAHKE' AND regdiv.value = 'K';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OMAHKE' AND regdiv.value = 'L';


	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OMUSTI' AND regdiv.value = 'A';


	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OSHANA' AND regdiv.value = 'A';


	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OSHKTO' AND regdiv.value = 'A';


	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OSHKTO' AND regdiv.value = 'B';


	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OTZNPA' AND regdiv.value = 'A';


	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OTZNPA' AND regdiv.value = 'B';


	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OTZNPA' AND regdiv.value = 'C';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OTZNPA' AND regdiv.value = 'D';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OTZNPA' AND regdiv.value = 'H';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OTZNPA' AND regdiv.value = 'J';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OTZNPA' AND regdiv.value = 'K';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'OTZNPA' AND regdiv.value = 'L';

	INSERT INTO cb_relevant_auth_reg_division (relv_auth_id, reg_division_id)
    SELECT ra.id, regdiv.id
    FROM cb_relevant_authority ra, cb_check_lht_reg_division regdiv
	WHERE ra.au_code = 'ZAMBZI' AND regdiv.value = 'B';

-- Populate the users table with the usernames from pg_catalog

	INSERT INTO cb_user (user_name, first_name, last_name)
	SELECT usename, usename, '' FROM pg_user;


----------------Create Logs and Triggers------------------------

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
  "juristic_person_number" varchar(50),
  "transfer_contract_number" varchar(30)
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
  "scheme_id" int4,
  "crs_id" int4,
  "scheme_field_book_id" int4
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

-- CREATE OR REPLACE FUNCTION cb_plot_num_to_int() RETURNS TRIGGER AS $cb_plot_num_to_int$
--     BEGIN
--         UPDATE cb_plot SET plot_number=(plot_number::INTEGER)::TEXT;
--         RETURN NULL;
--     END;
-- $cb_plot_num_to_int$ LANGUAGE plpgsql;

------ Timestamp

CREATE OR REPLACE FUNCTION insert_timestamp() RETURNS TRIGGER AS $insert_timestamp$
    BEGIN
        NEW.timestamp = NOW();
		RETURN NEW;
    END;

$insert_timestamp$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION flts_plot_num_to_numeric() RETURNS TRIGGER AS $flts_plot_num_to_numeric$
    BEGIN
        UPDATE cb_plot SET plot_number=(plot_number::INTEGER)::TEXT;
		RETURN NULL;
    END;

$flts_plot_num_to_numeric$ LANGUAGE plpgsql;

--- TRIGGERS

CREATE TRIGGER cb_scheme_log
AFTER INSERT OR UPDATE OR DELETE ON cb_scheme
    FOR EACH ROW EXECUTE PROCEDURE cb_scheme_log();

CREATE TRIGGER cb_holder_log
AFTER INSERT OR UPDATE OR DELETE ON cb_holder
    FOR EACH ROW EXECUTE PROCEDURE cb_holder_log();

-- CREATE TRIGGER cb_plot_num_to_int
-- AFTER INSERT OR UPDATE ON cb_plot
--     FOR EACH ROW EXECUTE PROCEDURE cb_plot_num_to_int();

CREATE TRIGGER cb_plot_log
AFTER UPDATE OR DELETE ON cb_plot
    FOR EACH ROW EXECUTE PROCEDURE cb_plot_log();

CREATE TRIGGER comment_timestamp
BEFORE INSERT OR UPDATE ON cb_comment
    FOR EACH ROW EXECUTE PROCEDURE insert_timestamp();

CREATE TRIGGER insert_workflow_timestamp
BEFORE INSERT OR UPDATE ON cb_scheme_workflow
    FOR EACH ROW EXECUTE PROCEDURE insert_timestamp();

CREATE TRIGGER plot_num_to_numeric
AFTER INSERT ON cb_plot
    FOR EACH ROW EXECUTE PROCEDURE flts_plot_num_to_numeric();



----------------Custom FLTS Functions------------------------

---Appends 'and' to the certificate preceding the spouse name
CREATE OR REPLACE FUNCTION "public"."flts_append_and_to_spouse_name"("holder_row" "public"."cb_holder")
  RETURNS "pg_catalog"."text" AS $BODY$BEGIN
	IF holder_row.marital_status = 1 THEN
		RETURN 'and';
	ELSE
		RETURN '';
	END IF;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

CREATE OR REPLACE FUNCTION "public"."flts_gen_holder_full_name"("holder_row" "public"."cb_holder")
  RETURNS "pg_catalog"."text" AS $BODY$DECLARE
BEGIN
	IF (holder_row.holder_first_name is null or holder_row.holder_first_name = '') THEN
		RETURN upper(holder_row.juristic_person_name);
	ELSE
		RETURN  upper(holder_row.holder_first_name) || ' ' || upper(holder_row.holder_surname);
	END IF;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

CREATE OR REPLACE FUNCTION "public"."flts_gen_holder_identity_number"("holder_row" "public"."cb_holder")
  RETURNS "pg_catalog"."text" AS $BODY$BEGIN
	IF (holder_row.holder_first_name is null or holder_row.holder_first_name = '') THEN
		RETURN 'Registration Number ' || holder_row.juristic_person_number;
	ELSE
		RETURN 'Identity Number ' || holder_row.holder_identifier;
	END IF;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

---Creates or populates certificate number when a certificate is generated
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
	RETURN 'LH'|| lpad(current_num::TEXT, 4, '0') || '/' || current_year;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

---Checks the nature of marriage for married holder
CREATE OR REPLACE FUNCTION "public"."flts_get_holder_nature_of_marriage"("holder_row" "public"."cb_holder")
  RETURNS "pg_catalog"."text" AS $BODY$DECLARE
	nature_of_marriage text;
BEGIN
	IF (holder_row.holder_first_name is null or holder_row.holder_first_name = '') THEN
		RETURN '';
	ELSE
		IF holder_row.marital_status = 1 THEN
			IF holder_row.nature_of_marriage = 1 THEN
				RETURN 'Married in community of property to each other.';
			ELSIF holder_row.nature_of_marriage = 2 THEN
				RETURN 'Married out of community of property.';
			ELSE
				RETURN 'Married, which marriage does not have the legal consequences of a marriage in community of property, by virtue of the provisions of Proclamation 15 of 1928.';
			END IF;
		ELSE
		RETURN 'Unmarried';
		END IF;
	END IF;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

-- Checks if scheme contains document imposing conditions and appends text in certificate
CREATE OR REPLACE FUNCTION "public"."flts_get_scheme_imposing_condition"("scheme_row" "public"."cb_scheme")
  RETURNS "pg_catalog"."text" AS $BODY$DECLARE
	doc_row cb_scheme_supporting_document%ROWTYPE;
	condition_txt TEXT := 'Subject to the conditions imposed by the ';
BEGIN
	SELECT * INTO doc_row FROM cb_scheme_supporting_document WHERE (cb_scheme_supporting_document.scheme_id = scheme_row.id AND cb_scheme_supporting_document.document_type = 7);
	IF doc_row IS NULL THEN
		RETURN '';
	ELSE
		RETURN condition_txt;
	END IF;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

CREATE OR REPLACE FUNCTION "public"."flts_get_scheme_imposing_condition2"("scheme_row" "public"."cb_scheme")
  RETURNS "pg_catalog"."text" AS $BODY$DECLARE
	doc_row cb_scheme_supporting_document%ROWTYPE;
	condition_txt TEXT := 'Registered in the Land Rights Office – Reference No. FK.';
BEGIN
	SELECT * INTO doc_row FROM cb_scheme_supporting_document WHERE (cb_scheme_supporting_document.scheme_id = scheme_row.id AND cb_scheme_supporting_document.document_type = 7);
	IF doc_row IS NULL THEN
		RETURN '';
	ELSE
		RETURN condition_txt || substr(scheme_row.scheme_number, 9) || ' S';
	END IF;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

--- Gets spouse national ID number from the database
CREATE OR REPLACE FUNCTION "public"."flts_get_spouse_document_identifier"("holder_row" "public"."cb_holder")
  RETURNS "pg_catalog"."text" AS $BODY$BEGIN
	IF holder_row.marital_status = 1 THEN
		RETURN 'Identity Number ' || holder_row.spouse_identifier;
	ELSE
		RETURN '';
	END IF;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

--- Gets spouse name from the database
CREATE OR REPLACE FUNCTION "public"."flts_get_spouse_name"("holder_row" "public"."cb_holder")
  RETURNS "pg_catalog"."text" AS $BODY$BEGIN
	IF holder_row.marital_status = 1 THEN
		RETURN upper(holder_row.spouse_first_name) || ' ' || upper(holder_row.spouse_surname);
	ELSE
		RETURN '';
	END IF;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

--- Creates an offset value if the certificate template text based on the marital status of the holder

CREATE OR REPLACE FUNCTION "public"."flts_marital_status_offset_value"("holder_row" "public"."cb_holder")
  RETURNS "pg_catalog"."text" AS $BODY$BEGIN
	IF holder_row.marital_status = 2 THEN
		RETURN 0;
	ELSEIF holder_row.marital_status IS NULL THEN
		RETURN -11;
	ELSE
		RETURN 25;
	END IF;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

--- Converts integer values to text
CREATE OR REPLACE FUNCTION "public"."flts_integer_to_text"(int4)
  RETURNS "pg_catalog"."text" AS $BODY$
    SELECT CASE
        WHEN $1=0 THEN 'Zero'
        WHEN $1=1 THEN 'One'
        WHEN $1=2 THEN 'Two'
        WHEN $1=3 THEN 'Three'
        WHEN $1=4 THEN 'Four'
        WHEN $1=5 THEN 'Five'
        WHEN $1=6 THEN 'Six'
        WHEN $1=7 THEN 'Seven'
        WHEN $1=8 THEN 'Eight'
        WHEN $1=9 THEN 'Nine'
		END
        $BODY$
  LANGUAGE sql IMMUTABLE STRICT
  COST 100;

--- Converts array of numbers to text

CREATE OR REPLACE FUNCTION "public"."flts_text_from_numbers"(int4)
  RETURNS "pg_catalog"."text" AS $BODY$
	DECLARE
    num_text text = cast($1 as text);
    text_num text [];
    name_num text;
	BEGIN
		FOR i IN 1.. length(num_text) LOOP
            name_num := "public".flts_integer_to_text( cast(substr(num_text,i,1) as int));
            text_num  := "pg_catalog".array_append(text_num, name_num );

        END LOOP;
	RETURN array_to_string(text_num, ' ');
END$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

--- Converts plot area value to text in the certificate
CREATE OR REPLACE FUNCTION "public"."flts_plot_area_to_text"("area" numeric)
  RETURNS "pg_catalog"."text" AS $BODY$DECLARE
	units VARCHAR(15);
	plot_area_txt TEXT;
	rounded_area INTEGER;
	measurement_txt TEXT := ', as shown and more fully described in the Land Hold Plan No. ';
BEGIN
	IF area < 10000 THEN
		rounded_area := round(area)::INTEGER;
		units := 'Square Meters';
	ELSE
		rounded_area := round(area/10000)::INTEGER;
		units := 'Hectares';
	END IF;

	RETURN rounded_area::TEXT || ' (' || flts_text_from_numbers(rounded_area) || ') ' || units || measurement_txt;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

CREATE OR REPLACE FUNCTION "public"."flts_ownership_text"("holder_row" "public"."cb_holder")
  RETURNS "pg_catalog"."text" AS $BODY$BEGIN
	IF holder_row.marital_status = 1 THEN
		RETURN 'their heirs, executors, administrators, or assigned, are the registered the holder(s) of';
	ELSE
		RETURN 'his/her heirs, executors, administrators, or assigned, is the registered the holder of';
	END IF;
END$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

CREATE OR REPLACE FUNCTION "public"."flts_gen_crs_text"("plot_row" "public"."cb_plot")
  RETURNS "pg_catalog"."text" AS $BODY$DECLARE
		BEGIN
			IF plot_row.crs_id = 1 THEN
				RETURN 'Lo22/13°';
			ELSIF plot_row.crs_id = 2 THEN
				RETURN 'Lo22/15°';
			ELSIF plot_row.crs_id = 3 THEN
				RETURN 'Lo22/17°';
			ELSIF plot_row.crs_id = 4 THEN
				RETURN 'Lo22/19°';
			ELSIF plot_row.crs_id = 5 THEN
				RETURN 'Lo22/21°';
			ELSIF plot_row.crs_id = 6 THEN
				RETURN 'Lo22/23°';
			ELSE
			RETURN 'Lo22/25°';
	END IF;
END;$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
  
----------------Custom FLTS Views------------------------

  /* A view for the search module. */
CREATE OR REPLACE VIEW cb_vw_plot_search AS
 SELECT cb_plot.id,
    cb_plot.upi,
    cb_plot.geom,
    cb_plot.plot_number,
--     cb_check_lht_plot_use.value AS plot_use,
    cb_plot.area,
    cb_scheme.scheme_name
   FROM cb_plot
--      JOIN cb_check_lht_plot_use ON cb_check_lht_plot_use.id = cb_plot.use
     JOIN cb_scheme ON cb_scheme.id = cb_plot.scheme_id;

CREATE OR REPLACE VIEW cb_vw_holder_search AS
    SELECT cb_holder.id,
        cb_holder.holder_first_name,
        cb_holder.holder_surname,
        cb_holder.holder_identifier
       FROM cb_holder;

CREATE OR REPLACE VIEW cb_vw_scheme_search AS
    SELECT cb_scheme.id,
        cb_scheme.scheme_name,
        cb_check_lht_region.value AS region,
        cb_scheme.date_of_establishment,
        cb_scheme.date_of_approval
       FROM cb_scheme
         JOIN cb_check_lht_region ON cb_check_lht_region.id = cb_scheme.region;

CREATE OR REPLACE VIEW cb_vw_juristic_search AS
     SELECT cb_holder.id,
        cb_holder.juristic_person_name,
        cb_holder.juristic_person_number
       FROM cb_holder;
	   
 /* A view for Holders report segregated by marital status. */
CREATE OR REPLACE VIEW cb_holder_vw_lht_report_marital_status_template AS
    SELECT 1 AS id,
        count(*) AS total_registered_holders,
        count(*) FILTER (WHERE ((cb_holder_vw_social_tenure_relationship.holder_marital_status)::text = 'Unmarried'::text)) AS unmarried_holders,
        count(*) FILTER (WHERE ((cb_holder_vw_social_tenure_relationship.holder_marital_status)::text = 'Married'::text)) AS married_holders,
        concat('Generated by ', CURRENT_USER, ' on ', LOCALTIMESTAMP(0)) AS user_time_text
    FROM cb_holder_vw_social_tenure_relationship;
	
/* A view for Holders report segregated by gender. */
CREATE OR REPLACE VIEW cb_holder_vw_lht_report_gender_template AS
    SELECT 1 AS id,
        count(*) AS total_registered_holders,
        count(*) FILTER (WHERE ((cb_holder_vw_social_tenure_relationship.holder_holder_gender)::text = 'Female'::text)) AS female,
        count(*) FILTER (WHERE ((cb_holder_vw_social_tenure_relationship.holder_holder_gender)::text = 'Male'::text)) AS male,
        concat('Generated by ', CURRENT_USER, ' on ', LOCALTIMESTAMP(0)) AS user_time_text
    FROM cb_holder_vw_social_tenure_relationship;

/* A view for Holders report segregated by disability status. */
CREATE OR REPLACE VIEW cb_holder_vw_lht_report_disability_template AS
    SELECT 1 AS id,
        count(*) AS total_registered_holders,
        count(*) FILTER (WHERE ((cb_holder_vw_social_tenure_relationship.holder_holder_disability_status)::text = 'Yes'::text)) AS holders_with_disability,
        count(*) FILTER (WHERE ((cb_holder_vw_social_tenure_relationship.holder_holder_disability_status)::text = 'No'::text)) AS holders_without_disability,
        concat('Generated by ', CURRENT_USER, ' on ', LOCALTIMESTAMP(0)) AS user_time_text
    FROM cb_holder_vw_social_tenure_relationship;


-- This creates the view for the certificate of Land Hold Title(LHT)
CREATE OR REPLACE VIEW cb_plot_vw_lht_certificate_template AS
  SELECT cb_plot.id,
    cb_scheme.scheme_number,
    flts_gen_cert_number() AS certificate_number,
    flts_ownership_text(cb_holder.*) AS ownership_text,
    concat('I, the Land Rights Registrar at ', cb_check_lht_land_rights_office.value, ', hereby certify that') AS land_rights_office_text,
    flts_gen_holder_full_name(cb_holder.*) AS full_name,
    flts_gen_holder_identity_number(cb_holder.*) AS holder_id,
    flts_append_and_to_spouse_name(cb_holder.*) AS append_and,
    flts_get_spouse_name(cb_holder.*) AS spouse_name,
    flts_get_spouse_document_identifier(cb_holder.*) AS spouse_document_identifier,
    flts_get_holder_nature_of_marriage(cb_holder.*) AS nature_of_marriage,
    concat('Plot No: ', (cb_plot.plot_number)::integer, ', ', cb_scheme.scheme_description) AS plot_number_description,
    concat(cb_scheme.scheme_name, ' Scheme') AS scheme_name,
    concat(cb_relevant_authority.name_of_relevant_authority, ' ', cb_check_lht_relevant_authority.value) AS authority,
    concat('Registration Division ', cb_check_lht_reg_division.value) AS reg_division,
    concat(cb_check_lht_region.value, ' Region') AS region,
    concat(flts_plot_area_to_text(cb_plot.area), cb_scheme.land_hold_plan_number, ';') AS area_in_words,
    concat(flts_get_scheme_imposing_condition(cb_scheme.*), cb_relevant_authority.name_of_relevant_authority, ' ', cb_check_lht_relevant_authority.value, ' in terms of section 13(6) of the Flexible Land Tenure Act, 2012.') AS imposing_condition_text,
    flts_get_scheme_imposing_condition2(cb_scheme.*) AS imposing_condition_text2,
    cb_scheme.land_hold_plan_number,
    concat('No. ', cb_scheme.land_hold_plan_number) AS land_hold_plan_no_text,
    concat('Plot No: ', (cb_plot.plot_number)::integer, ', ', cb_scheme.scheme_name, ' Scheme, ', flts_gen_crs_text(cb_plot.*)) AS plot_scheme_text,
    concat(rtrim((cb_check_lht_relevant_authority.value)::text, 'Council'::text), 'of ', cb_relevant_authority.name_of_relevant_authority, ', ', cb_check_lht_region.value, ' Region') AS ra_region,
    concat('Plot No: ', (cb_plot.plot_number)::integer) AS plot_number,
    cb_plot.upi AS plot_upi,
    cb_plot.geom AS plot_geom,
    flts_marital_status_offset_value(cb_holder.*) AS marital_status_offset_value
   FROM ((((((((cb_social_tenure_relationship
     JOIN cb_plot ON ((cb_social_tenure_relationship.plot_id = cb_plot.id)))
     JOIN cb_scheme ON ((cb_plot.scheme_id = cb_scheme.id)))
     JOIN cb_check_lht_land_rights_office ON ((cb_scheme.land_rights_office = cb_check_lht_land_rights_office.id)))
     JOIN cb_holder ON ((cb_social_tenure_relationship.holder_id = cb_holder.id)))
     JOIN cb_relevant_authority ON (((cb_relevant_authority.au_code)::text = 'OSHKTI'::text)))
     JOIN cb_check_lht_relevant_authority ON ((cb_check_lht_relevant_authority.id = cb_scheme.relevant_authority)))
     JOIN cb_check_lht_reg_division ON ((cb_check_lht_reg_division.id = cb_scheme.registration_division)))
     JOIN cb_check_lht_region ON ((cb_check_lht_region.id = cb_scheme.region)))
		
----------------------END-------------------------------------