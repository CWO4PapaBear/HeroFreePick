-- Fresh installation only. Existing test installations retain these tables unchanged.
CREATE TABLE hero_starting_path_test (
 guid INT UNSIGNED NOT NULL PRIMARY KEY,
 account_id INT UNSIGNED NOT NULL,
 character_name VARCHAR(12) NOT NULL,
 class_id TINYINT UNSIGNED NOT NULL,
 phase TINYINT UNSIGNED NOT NULL DEFAULT 0,
 snapshot_count INT UNSIGNED NOT NULL,
 held_count INT UNSIGNED NOT NULL
) ENGINE=InnoDB;
CREATE TABLE hero_starting_path_spells_test (
 guid INT UNSIGNED NOT NULL,
 spell INT UNSIGNED NOT NULL,
 spec_mask TINYINT UNSIGNED NOT NULL,
 withheld TINYINT UNSIGNED NOT NULL,
 PRIMARY KEY(guid,spell)
) ENGINE=InnoDB;
CREATE TABLE hero_build_test (
 guid INT UNSIGNED NOT NULL PRIMARY KEY,
 revision INT UNSIGNED NOT NULL DEFAULT 0,
 catalog INT UNSIGNED NOT NULL DEFAULT 37033160,
 selections VARCHAR(6144) NOT NULL DEFAULT '-'
) ENGINE=InnoDB;
CREATE TABLE hero_build_spells_test (
 guid INT UNSIGNED NOT NULL,
 spell INT UNSIGNED NOT NULL,
 owned_before TINYINT UNSIGNED NOT NULL,
 PRIMARY KEY(guid,spell)
) ENGINE=InnoDB;
