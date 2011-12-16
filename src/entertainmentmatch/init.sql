/home/likees/likees/src/entertainmentmatch/likees/media/
/home/likees/likees/src/entertainmentmatch/likees/media/
BEGIN;
CREATE TABLE `likees_user_networks` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `socialnetworkplatform_id` integer NOT NULL,
    UNIQUE (`user_id`, `socialnetworkplatform_id`)
)
;
CREATE TABLE `likees_user_soulmates` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `from_user_id` integer NOT NULL,
    `to_user_id` integer NOT NULL,
    UNIQUE (`from_user_id`, `to_user_id`)
)
;
CREATE TABLE `likees_user_friends` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `from_user_id` integer NOT NULL,
    `to_user_id` integer NOT NULL,
    UNIQUE (`from_user_id`, `to_user_id`)
)
;
CREATE TABLE `likees_user` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `email` varchar(100) NOT NULL,
    `username` varchar(100) NOT NULL,
    `password` varchar(100) NOT NULL,
    `gender` varchar(10) NOT NULL,
    `birthdate` date NOT NULL,
    `is_active` bool NOT NULL,
    `num_login_try` integer NOT NULL,
    `last_login_date` date NOT NULL,
    `name` varchar(100) NOT NULL,
    `surname` varchar(100) NOT NULL,
    `page_language_id` integer NOT NULL,
    `image_id` integer NOT NULL
)
;
ALTER TABLE `likees_user_networks` ADD CONSTRAINT `user_id_refs_id_766b0164` FOREIGN KEY (`user_id`) REFERENCES `likees_user` (`id`);
ALTER TABLE `likees_user_soulmates` ADD CONSTRAINT `from_user_id_refs_id_774e9db9` FOREIGN KEY (`from_user_id`) REFERENCES `likees_user` (`id`);
ALTER TABLE `likees_user_soulmates` ADD CONSTRAINT `to_user_id_refs_id_774e9db9` FOREIGN KEY (`to_user_id`) REFERENCES `likees_user` (`id`);
ALTER TABLE `likees_user_friends` ADD CONSTRAINT `from_user_id_refs_id_4c8b1e81` FOREIGN KEY (`from_user_id`) REFERENCES `likees_user` (`id`);
ALTER TABLE `likees_user_friends` ADD CONSTRAINT `to_user_id_refs_id_4c8b1e81` FOREIGN KEY (`to_user_id`) REFERENCES `likees_user` (`id`);
CREATE TABLE `likees_item_produced` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `item_id` integer NOT NULL,
    `country_id` varchar(2) NOT NULL,
    UNIQUE (`item_id`, `country_id`)
)
;
CREATE TABLE `likees_item_categories` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `item_id` integer NOT NULL,
    `category_id` integer NOT NULL,
    UNIQUE (`item_id`, `category_id`)
)
;
CREATE TABLE `likees_item` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `released` date,
    `buy_links` varchar(100),
    `rating` double precision,
    `homepage` varchar(100),
    `votes_count` integer,
    `version` integer,
    `name_code_m` integer,
    `name_default_m` varchar(100) NOT NULL,
    `alternative_name_code_m` integer,
    `alternative_name_default_m` varchar(100),
    `overview_code_m` integer,
    `overview_default_m` longtext,
    `review_code_m` integer,
    `review_default_m` longtext,
    `parent_item` integer,
    `tagline_code_m` integer,
    `tagline_default_m` longtext,
    `type` varchar(50),
    `image_id` integer,
    `thumb_id` integer
)
;
ALTER TABLE `likees_item_produced` ADD CONSTRAINT `item_id_refs_id_3f803ea3` FOREIGN KEY (`item_id`) REFERENCES `likees_item` (`id`);
ALTER TABLE `likees_item_categories` ADD CONSTRAINT `item_id_refs_id_6911f0fd` FOREIGN KEY (`item_id`) REFERENCES `likees_item` (`id`);
CREATE TABLE `likees_movie` (
    `item_ptr_id` integer NOT NULL PRIMARY KEY,
    `runtime` integer,
    `trailer` varchar(200),
    `id_imdb` varchar(10),
    `id_tmdb` integer
)
;
ALTER TABLE `likees_movie` ADD CONSTRAINT `item_ptr_id_refs_id_135e5171` FOREIGN KEY (`item_ptr_id`) REFERENCES `likees_item` (`id`);
CREATE TABLE `likees_company` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(100) NOT NULL
)
;
CREATE TABLE `likees_role` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `item_id` integer NOT NULL,
    `company_id` integer NOT NULL,
    `name_code_m` integer,
    `name_default_m` longtext
)
;
ALTER TABLE `likees_role` ADD CONSTRAINT `company_id_refs_id_312b87eb` FOREIGN KEY (`company_id`) REFERENCES `likees_company` (`id`);
ALTER TABLE `likees_role` ADD CONSTRAINT `item_id_refs_id_7f7654d6` FOREIGN KEY (`item_id`) REFERENCES `likees_item` (`id`);
CREATE TABLE `likees_vote` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `item_id` integer NOT NULL,
    `rate` integer NOT NULL,
    `date` date NOT NULL
)
;
ALTER TABLE `likees_vote` ADD CONSTRAINT `item_id_refs_id_5f035802` FOREIGN KEY (`item_id`) REFERENCES `likees_item` (`id`);
ALTER TABLE `likees_vote` ADD CONSTRAINT `user_id_refs_id_187c93d6` FOREIGN KEY (`user_id`) REFERENCES `likees_user` (`id`);
CREATE TABLE `likees_critic` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `item_id` integer NOT NULL,
    `text` longtext NOT NULL,
    `date` date NOT NULL
)
;
ALTER TABLE `likees_critic` ADD CONSTRAINT `item_id_refs_id_198b405c` FOREIGN KEY (`item_id`) REFERENCES `likees_item` (`id`);
ALTER TABLE `likees_critic` ADD CONSTRAINT `user_id_refs_id_3d7a3e88` FOREIGN KEY (`user_id`) REFERENCES `likees_user` (`id`);
CREATE TABLE `likees_job` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name_code_m` integer,
    `name_default_m` longtext NOT NULL
)
;
CREATE TABLE `likees_person` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(100) NOT NULL,
    `image_id` integer
)
;
CREATE TABLE `likees_cast` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `character_code_m` integer,
    `character_default_m` longtext NOT NULL
)
;
CREATE TABLE `likees_item_job_cast_person` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `person_id` integer NOT NULL,
    `item_id` integer NOT NULL,
    `job_id` integer NOT NULL,
    `cast_id` integer
)
;
ALTER TABLE `likees_item_job_cast_person` ADD CONSTRAINT `cast_id_refs_id_14d6791f` FOREIGN KEY (`cast_id`) REFERENCES `likees_cast` (`id`);
ALTER TABLE `likees_item_job_cast_person` ADD CONSTRAINT `item_id_refs_id_7fa07cc1` FOREIGN KEY (`item_id`) REFERENCES `likees_item` (`id`);
ALTER TABLE `likees_item_job_cast_person` ADD CONSTRAINT `job_id_refs_id_1a3de246` FOREIGN KEY (`job_id`) REFERENCES `likees_job` (`id`);
ALTER TABLE `likees_item_job_cast_person` ADD CONSTRAINT `person_id_refs_id_5b55d853` FOREIGN KEY (`person_id`) REFERENCES `likees_person` (`id`);
CREATE TABLE `likees_category` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name_code_m` integer,
    `name_default_m` longtext NOT NULL,
    `parent_category_id` integer
)
;
ALTER TABLE `likees_item_categories` ADD CONSTRAINT `category_id_refs_id_501ed3a8` FOREIGN KEY (`category_id`) REFERENCES `likees_category` (`id`);
ALTER TABLE `likees_category` ADD CONSTRAINT `parent_category_id_refs_id_3cd1c685` FOREIGN KEY (`parent_category_id`) REFERENCES `likees_category` (`id`);
CREATE TABLE `likees_item_tag_user` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `item_id` integer NOT NULL,
    `tag_id` integer NOT NULL,
    `user_id` integer NOT NULL
)
;
ALTER TABLE `likees_item_tag_user` ADD CONSTRAINT `item_id_refs_id_5124a695` FOREIGN KEY (`item_id`) REFERENCES `likees_item` (`id`);
ALTER TABLE `likees_item_tag_user` ADD CONSTRAINT `user_id_refs_id_6c8ba4c1` FOREIGN KEY (`user_id`) REFERENCES `likees_user` (`id`);
CREATE TABLE `likees_tag` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(100) NOT NULL
)
;
ALTER TABLE `likees_item_tag_user` ADD CONSTRAINT `tag_id_refs_id_3a2a0687` FOREIGN KEY (`tag_id`) REFERENCES `likees_tag` (`id`);
CREATE TABLE `likees_image` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `url` varchar(200) NOT NULL,
    `date` date NOT NULL
)
;
ALTER TABLE `likees_user` ADD CONSTRAINT `image_id_refs_id_49f718ec` FOREIGN KEY (`image_id`) REFERENCES `likees_image` (`id`);
ALTER TABLE `likees_item` ADD CONSTRAINT `image_id_refs_id_2480c10` FOREIGN KEY (`image_id`) REFERENCES `likees_image` (`id`);
ALTER TABLE `likees_item` ADD CONSTRAINT `thumb_id_refs_id_2480c10` FOREIGN KEY (`thumb_id`) REFERENCES `likees_image` (`id`);
ALTER TABLE `likees_person` ADD CONSTRAINT `image_id_refs_id_68280b14` FOREIGN KEY (`image_id`) REFERENCES `likees_image` (`id`);
CREATE TABLE `likees_socialnetworkplatform` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `token` varchar(100) NOT NULL
)
;
ALTER TABLE `likees_user_networks` ADD CONSTRAINT `socialnetworkplatform_id_refs_id_2c76441e` FOREIGN KEY (`socialnetworkplatform_id`) REFERENCES `likees_socialnetworkplatform` (`id`);
CREATE TABLE `likees_pagelanguage` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(2) NOT NULL
)
;
ALTER TABLE `likees_user` ADD CONSTRAINT `page_language_id_refs_id_3547b3e5` FOREIGN KEY (`page_language_id`) REFERENCES `likees_pagelanguage` (`id`);
CREATE TABLE `likees_country` (
    `id` varchar(2) NOT NULL PRIMARY KEY,
    `name_code_m` integer,
    `name_default_m` longtext NOT NULL,
    `flag_url` varchar(100)
)
;
ALTER TABLE `likees_item_produced` ADD CONSTRAINT `country_id_refs_id_321c2f41` FOREIGN KEY (`country_id`) REFERENCES `likees_country` (`id`);
CREATE TABLE `likees_releasedate` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `date` date NOT NULL,
    `release_on` varchar(10) NOT NULL
)
;
CREATE TABLE `likees_item_releasedate_country` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `item_id` integer NOT NULL,
    `releaseDate_id` integer NOT NULL,
    `country_id` varchar(2) NOT NULL
)
;
ALTER TABLE `likees_item_releasedate_country` ADD CONSTRAINT `releaseDate_id_refs_id_77b0f9af` FOREIGN KEY (`releaseDate_id`) REFERENCES `likees_releasedate` (`id`);
ALTER TABLE `likees_item_releasedate_country` ADD CONSTRAINT `item_id_refs_id_5d9e460e` FOREIGN KEY (`item_id`) REFERENCES `likees_item` (`id`);
ALTER TABLE `likees_item_releasedate_country` ADD CONSTRAINT `country_id_refs_id_3cedc75c` FOREIGN KEY (`country_id`) REFERENCES `likees_country` (`id`);
CREATE TABLE `likees_multilanguage` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `code` integer NOT NULL,
    `language` varchar(10) NOT NULL,
    `literal` longtext NOT NULL,
    UNIQUE (`code`, `language`)
)
;
insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('AD', 'Andorra', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('AE', 'Emiratos Árabes Unidos', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('AF', 'Afganistán', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('AG', 'Antigua y Barbuda', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('AI', 'Anguila', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('AL', 'Albania', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('AM', 'Armenia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('AN', 'Antillas Neerlandesas', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('AO', 'Angola', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('AQ', 'Antártida', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('AR', 'Argentina', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('AS', 'Samoa Americana', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('AT', 'Austria', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('AU', 'Australia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('AW', 'Aruba', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('AZ', 'Azerbaiyán', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('BA', 'Bosnia y Hercegovina', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('BB', 'Barbados', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('BD', 'Bangladesh', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('BE', 'Bélgica', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('BF', 'Burkina Faso', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('BG', 'Bulgaria', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('BH', 'Bahráin', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('BI', 'Burundi', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('BJ', 'Benín', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('BM', 'Bermudas', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('BN', 'Brunéi', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('BO', 'Bolivia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('BR', 'Brasil', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('BS', 'Bahamas', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('BT', 'Bután', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('BV', 'Isla Bouvet', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('BW', 'Botsuana', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('BY', 'Bielorrusia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('BZ', 'Belice', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('CA', 'Canadá', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('CC', 'Islas Cocos', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('CD', 'República Democrática del Congo', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('CF', 'República Centroafricana', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('CG', 'Congo', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('CI', 'Costa de Marfil', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('CK', 'Islas Cook', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('CL', 'Chile', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('CM', 'Camerún', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('CN', 'China', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('CO', 'Colombia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('CR', 'Costa Rica', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('CU', 'Cuba', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('CV', 'Cabo Verde', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('CX', 'Isla Christmas', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('CY', 'Chipre', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('CZ', 'República Checa; Chequia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('CH', 'Suiza', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('DE', 'Alemania', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('DJ', 'Yibuti', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('DK', 'Dinamarca', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('DM', 'Dominica', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('DO', 'República Dominicana', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('DZ', 'Argelia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('EC', 'Ecuador', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('EE', 'Estonia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('EG', 'Egipto', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('EH', 'Sáhara Occidental', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('ER', 'Eritrea', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('ES', 'España', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('ET', 'Etiopía', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('FI', 'Finlandia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('FJ', 'Fiyi', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('FK', 'Islas Malvinas', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('FM', 'Micronesia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('FO', 'Islas Feroe', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('FR', 'Francia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('GA', 'Gabón', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('GB', 'Reino Unido', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('GD', 'Granada', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('GE', 'Georgia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('GF', 'Guayana Francesa', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('GH', 'Ghana', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('GI', 'Gibraltar', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('GL', 'Groenlandia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('GM', 'Gambia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('GN', 'Guinea', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('GP', 'Guadalupe', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('GQ', 'Guinea Ecuatorial', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('GR', 'Grecia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('GS', 'Islas Georgia del Sur y Sandwich del Sur', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('GT', 'Guatemala', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('GU', 'Guam', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('GW', 'Guinea-Bissau', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('GY', 'Guyana', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('HM', 'Islas Heard y McDonald', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('HN', 'Honduras', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('HR', 'Croacia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('HT', 'Haití', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('HU', 'Hungría', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('ID', 'Indonesia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('IE', 'Irlanda', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('IL', 'Israel', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('IN', 'India', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('IO', 'Territorio Británico del Océano Índico', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('IQ', 'Iraq', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('IR', 'Irán', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('IS', 'Islandia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('IT', 'Italia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('JM', 'Jamaica', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('JO', 'Jordania', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('JP', 'Japón', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('KE', 'Kenia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('KG', 'Kirguizistán', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('KH', 'Camboya', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('KI', 'Kiribati', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('UY', 'Uruguay', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('UZ', 'Uzbekistán', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('VA', 'El Vaticano', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('VC', 'San Vicente y las Granadinas', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('VE', 'Venezuela', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('VG', 'Islas Vírgenes Británicas', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('VI', 'Islas Vírgenes Americanas', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('VN', 'Vietnam', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('VU', 'Vanuatu', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('WF', 'Wallis y Futuna', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('WS', 'Samoa', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('YE', 'Yemen', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('YT', 'Mayotte', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('YU', 'Serbia y Montenegro', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('ZA', 'Sudáfrica', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('ZM', 'Zambia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('ZW', 'Zimbabue', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('KM', 'Comoras', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('KN', 'San Cristóbal y Nieves', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('KP', 'Corea del Norte', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('KR', 'Corea del Sur', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('KW', 'Kuwait', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('KY', 'Islas Caimán', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('KZ', 'Kazajistán', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('LA', 'Laos', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('LB', 'Líbano', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('LC', 'Santa Lucía', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('LI', 'Liechtenstein', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('LK', 'Sri Lanka', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('LR', 'Liberia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('LS', 'Lesoto', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('LT', 'Lituania', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('LU', 'Luxemburgo', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('LV', 'Letonia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('LY', 'Libia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('MA', 'Marruecos', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('MC', 'Mónaco', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('MD', 'Moldavia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('MG', 'Madagascar', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('MH', 'Islas Marshall', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('MK', 'Macedonia; Antigua República Yugoslava de Macedonia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('ML', 'Malí', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('MM', 'Birmania; Myanmar', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('MN', 'Mongolia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('MO', 'Macao', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('MP', 'Islas Marianas del Norte', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('MQ', 'Martinica', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('MR', 'Mauritania', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('MS', 'Montserrat', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('MT', 'Malta', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('MU', 'Mauricio', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('MV', 'Maldivas', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('MW', 'Malaui', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('MX', 'México', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('MY', 'Malasia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('MZ', 'Mozambique', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('NA', 'Namibia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('NC', 'Nueva Caledonia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('NE', 'Níger', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('NF', 'Isla Norfolk', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('NG', 'Nigeria', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('NI', 'Nicaragua', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('NL', 'Países Bajos', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('NO', 'Noruega', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('NP', 'Nepal', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('NR', 'Nauru', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('NU', 'Niue', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('NZ', 'Nueva Zelanda', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('OM', 'Omán', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('PA', 'Panamá', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('PE', 'Perú', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('PF', 'Polinesia Francesa', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('PG', 'Papúa-Nueva Guinea', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('PH', 'Filipinas', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('PK', 'Pakistán', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('PL', 'Polonia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('PM', 'San Pedro y Miquelón', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('PN', 'Islas Pitcairn', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('PR', 'Puerto Rico', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('PT', 'Portugal', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('PW', 'Palaos', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('PY', 'Paraguay', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('QA', 'Qatar', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('RE', 'Reunión', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('RO', 'Rumania; Rumanía', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('RU', 'Rusia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('RW', 'Ruanda', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('SA', 'Arabia Saudí', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('SB', 'Islas Salomón', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('SC', 'Seychelles', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('SD', 'Sudán', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('SE', 'Suecia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('SG', 'Singapur', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('SH', 'Santa Helena', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('SI', 'Eslovenia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('SJ', 'Svalbard y Jan Mayen', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('SK', 'Eslovaquia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('SL', 'Sierra Leona', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('SM', 'San Marino', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('SN', 'Senegal', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('SO', 'Somalia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('SR', 'Surinam', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('ST', 'Santo Tomé y Príncipe', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('SV', 'El Salvador', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('SY', 'Siria', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('SZ', 'Suazilandia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('TC', 'Islas Turcas y Caicos', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('TD', 'Chad', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('TF', 'Territorios Australes Franceses', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('TG', 'Togo', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('TH', 'Tailandia', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('TJ', 'Tayikistán', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('TK', 'Tokelau', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('TL', 'Timor Oriental', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('TM', 'Turkmenistán', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('TN', 'Túnez', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('TO', 'Tonga', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('TR', 'Turquía', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('TT', 'Trinidad y Tobago', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('TV', 'Tuvalu', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('TW', 'Taiwán', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('TZ', 'Tanzania', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('UA', 'Ucrania', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('UG', 'Uganda', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('UM', 'Islas menores alejadas de los Estados Unidos', null, '');

insert into likees_country (ID, NAME_DEFAULT_M, NAME_CODE_M, FLAG_URL) values ('US', 'Estados Unidos', null, '');
CREATE INDEX `likees_user_5bc87959` ON `likees_user` (`page_language_id`);
CREATE INDEX `likees_user_6682136` ON `likees_user` (`image_id`);
CREATE INDEX `likees_item_6682136` ON `likees_item` (`image_id`);
CREATE INDEX `likees_item_5be5f78d` ON `likees_item` (`thumb_id`);
CREATE INDEX `likees_role_67b70d25` ON `likees_role` (`item_id`);
CREATE INDEX `likees_role_543518c6` ON `likees_role` (`company_id`);
CREATE INDEX `likees_vote_403f60f` ON `likees_vote` (`user_id`);
CREATE INDEX `likees_vote_67b70d25` ON `likees_vote` (`item_id`);
CREATE INDEX `likees_critic_403f60f` ON `likees_critic` (`user_id`);
CREATE INDEX `likees_critic_67b70d25` ON `likees_critic` (`item_id`);
CREATE INDEX `likees_person_6682136` ON `likees_person` (`image_id`);
CREATE INDEX `likees_item_job_cast_person_21b911c5` ON `likees_item_job_cast_person` (`person_id`);
CREATE INDEX `likees_item_job_cast_person_67b70d25` ON `likees_item_job_cast_person` (`item_id`);
CREATE INDEX `likees_item_job_cast_person_751f44ae` ON `likees_item_job_cast_person` (`job_id`);
CREATE INDEX `likees_item_job_cast_person_22c7b3db` ON `likees_item_job_cast_person` (`cast_id`);
CREATE INDEX `likees_category_6bb36718` ON `likees_category` (`parent_category_id`);
CREATE INDEX `likees_item_tag_user_67b70d25` ON `likees_item_tag_user` (`item_id`);
CREATE INDEX `likees_item_tag_user_3747b463` ON `likees_item_tag_user` (`tag_id`);
CREATE INDEX `likees_item_tag_user_403f60f` ON `likees_item_tag_user` (`user_id`);
CREATE INDEX `likees_item_releasedate_country_67b70d25` ON `likees_item_releasedate_country` (`item_id`);
CREATE INDEX `likees_item_releasedate_country_2645994c` ON `likees_item_releasedate_country` (`releaseDate_id`);
CREATE INDEX `likees_item_releasedate_country_534dd89` ON `likees_item_releasedate_country` (`country_id`);
COMMIT;
