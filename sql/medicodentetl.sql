DROP TABLE IF EXISTS `table_type_patient`;

CREATE TABLE `table_type_patient` (
  `id_patient` int(8) NOT NULL,
  `type_patient` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
