DROP TABLE IF EXISTS `table_type_patient`;
DROP TABLE IF EXISTS `table_type_paiement`;
DROP TABLE IF EXISTS `table_type_jour`;

-- --------------------------------------------------------

--
-- Structure de la table `table_type_patient`
--
CREATE TABLE `table_type_patient` (
  `id_patient` int(8) NOT NULL,
  `type_patient` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Index pour la table `table_type_patient`
--
ALTER TABLE `table_type_patient`
  ADD PRIMARY KEY (`id_patient`);

--
-- Structure de la table `table_type_paiement`
--
CREATE TABLE `table_type_paiement` (
  `id_paiement` int(8) NOT NULL,
  `type_paiement` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Index pour la table `table_type_paiement`
--
ALTER TABLE `table_type_paiement`
  ADD PRIMARY KEY (`id_paiement`);
  
--
-- Structure de la table `table_type_jour`
--

CREATE TABLE `table_type_jour` (
  `id_t_jour` int(8) NOT NULL,
  `type_jour` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
 
--
-- Index pour la table `table_type_jour`
--
ALTER TABLE `table_type_jour`
  ADD PRIMARY KEY (`id_t_jour`);
