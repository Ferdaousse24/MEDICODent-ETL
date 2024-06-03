DROP TABLE IF EXISTS `table_type_patient`;
DROP TABLE IF EXISTS `table_type_paiement`;
DROP TABLE IF EXISTS `table_type_jour`;
DROP TABLE IF EXISTS `table_t_mois`;
DROP TABLE IF EXISTS `table_t_semaine`;
DROP TABLE IF EXISTS `table_t_annee`;

-- --------------------------------------------------------

-- Structure de la table `table_type_patient`
--
CREATE TABLE `table_type_patient` (
  `id_patient` int(8) NOT NULL,
  `type_patient` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Index pour la table `table_type_patient`
--
ALTER TABLE `table_type_patient`
  ADD PRIMARY KEY (`id_patient`);

-- Structure de la table `table_type_paiement`
--
CREATE TABLE `table_type_paiement` (
  `id_paiement` int(8) NOT NULL,
  `type_paiement` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Index pour la table `table_type_paiement`
--
ALTER TABLE `table_type_paiement`
  ADD PRIMARY KEY (`id_paiement`);
  
-- Structure de la table `table_type_jour`
--
CREATE TABLE `table_type_jour` (
  `id_t_jour` int(8) NOT NULL,
  `type_jour` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
 
-- Index pour la table `table_type_jour`
--
ALTER TABLE `table_type_jour`
  ADD PRIMARY KEY (`id_t_jour`);

-- Structure de la table `table_t_annee`
--
CREATE TABLE `table_t_annee` (
  `id_A` int(4) NOT NULL,
  `annee` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Index pour la table `table_t_annee`
--
ALTER TABLE `table_t_annee`
  ADD PRIMARY KEY (`id_A`);

-- Structure de la table `table_t_mois`
--
CREATE TABLE `table_t_mois` (
  `id_M` int(4) NOT NULL,
  `mois` int(4) NOT NULL,
  `id_A` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Index pour la table `table_t_mois`
--
ALTER TABLE `table_t_mois`
  ADD PRIMARY KEY (`id_M`);
  
-- Contraintes pour la table `table_t_mois`
--
ALTER TABLE `table_t_mois`
  ADD CONSTRAINT `ContrainteFromAnneeMois` FOREIGN KEY (`id_A`) REFERENCES `table_t_annee` (`id_A`);

-- Structure de la table `table_t_semaine`
--
CREATE TABLE `table_t_semaine` (
  `id_S` int(8) NOT NULL,
  `semaine` int(8) NOT NULL,
  `id_A` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Index pour la table `table_t_semaine`
--
ALTER TABLE `table_t_semaine`
  ADD PRIMARY KEY (`id_S`);

-- Contraintes pour la table `table_t_semaine`
--
ALTER TABLE `table_t_semaine`
  ADD CONSTRAINT `ContrainteFromAnneeSemaine` FOREIGN KEY (`id_A`) REFERENCES `table_t_annee` (`id_A`);
