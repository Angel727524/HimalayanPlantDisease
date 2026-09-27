-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: himalayan_plant_disease
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `admin_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(200) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `diseases`
--

DROP TABLE IF EXISTS `diseases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `diseases` (
  `disease_id` int NOT NULL AUTO_INCREMENT,
  `disease_name` varchar(150) NOT NULL,
  `disease_type` varchar(100) DEFAULT NULL,
  `description` text,
  `cause` text,
  `symptoms` text,
  `treatment` text,
  `prevention` text,
  `severity` enum('Low','Medium','High') DEFAULT 'Medium',
  `reference_source` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`disease_id`),
  UNIQUE KEY `disease_name` (`disease_name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `diseases`
--

LOCK TABLES `diseases` WRITE;
/*!40000 ALTER TABLE `diseases` DISABLE KEYS */;
INSERT INTO `diseases` VALUES (1,'Leaf Spot Disease','Fungal / Bacterial','Leaf spot is a general disease symptom in which localized spots or lesions develop on leaves. Different fungal and bacterial pathogens can cause leaf spot, and the specific pathogen varies according to the host plant.','Common causes include fungal and bacterial pathogens. Infected plant debris, splashing water, rain, high humidity, and poor air circulation can contribute to disease development and spread.','Small tan, brown, reddish-brown, black, or yellow spots may appear on leaves. Spots can enlarge and merge into larger lesions. Severe infections may cause yellowing, leaf drop, or dieback.','Remove and destroy severely infected leaves and plant material. Improve air circulation and reduce leaf wetness. Water plants in a way that keeps foliage as dry as possible. Appropriate fungicides or bactericides may be considered when suitable for the identified pathogen and host plant.','Remove fallen infected leaves and plant debris. Avoid overhead watering when possible. Maintain good spacing and air circulation. Inspect plants regularly and remove infected material early.','Medium','University of Maryland Extension - Fungal Leaf Spots: https://www.extension.umd.edu/resource/fungal-leaf-spots-indoor-plants ; University of Georgia Extension - Leaf Spot: https://site.extension.uga.edu/lincoln/whats-that-disease-leaf-spot/','2026-09-26 16:40:58','2026-09-26 16:57:32'),(2,'Powdery Mildew','Fungal','Powdery mildew is a group of fungal diseases that produces a characteristic white or gray powdery growth on plant leaves and shoots.','Caused by several groups of powdery mildew fungi. Moderate temperatures, humidity, shade, and poor air circulation can favor disease development.','White or gray powder-like growth appears on the surface of leaves and shoots. Leaves may become yellow or brown, curl, become distorted, and eventually fall.','Remove severely infected leaves and plant parts. Improve air circulation and growing conditions. For susceptible plants, an appropriate registered fungicide may be used according to the product label and plant requirements.','Provide adequate spacing between plants, improve air circulation, avoid excessive shading, and monitor plants regularly for early symptoms.','Medium','Iowa State University Extension - Powdery Mildew: https://yardandgarden.extension.iastate.edu/encyclopedia/powdery-mildew-ornamental-plants ; University of Maryland Extension - Powdery Mildew: https://www.extension.umd.edu/resource/powdery-mildew-indoor-plants ; UC IPM - Powdery Mildew: https://ipm.ucanr.edu/home-and-landscape/powdery-mildew-on-ornamentals/','2026-09-26 16:40:58','2026-09-26 16:57:32'),(3,'Rust Disease','Fungal','Rust disease is a group of fungal diseases that commonly produces yellow, orange, reddish, or brown spots and spore-producing structures on plant tissues.','Caused by rust fungi belonging to several genera, including Puccinia, Uromyces, and related groups. Some rust fungi require more than one host species to complete their life cycle.','Small yellow, orange, red, or brown spots or raised pustules may develop on leaves or stems. Orange or rust-colored spores may be visible, particularly on the underside of leaves. Severe infections can cause yellowing, browning, and premature leaf death.','Remove and destroy severely infected plant material. Improve air circulation and avoid prolonged leaf wetness. Where appropriate, a registered fungicide can be used according to the product label and the specific host-pathogen combination.','Inspect plants regularly, remove infected leaves and plant debris, improve air circulation, and avoid unnecessary overhead watering.','Medium','Penn State Extension - Rust Diseases: https://extension.psu.edu/turfgrass-diseases-rust-diseases-causal-fungi-puccinia-spp ; University of Minnesota Extension - Rust Symptoms: https://apps.extension.umn.edu/garden/diagnose/plant/annualperennial/grass/','2026-09-26 16:40:58','2026-09-26 16:57:32'),(4,'Root Rot','Fungal / Oomycete','Root rot is a disease condition in which plant roots become damaged, discolored, and decayed. It is frequently associated with excessive moisture and poorly drained soil.','Can be caused by several soil-borne fungi and fungus-like organisms including Pythium, Phytophthora, Rhizoctonia, and Fusarium. Excessive moisture and poor drainage can increase disease risk.','Plants may show wilting, yellowing, poor growth, leaf browning, and dieback. Diseased roots may become brown or black, soft, and damaged.','Improve soil drainage and avoid excessive watering. Remove severely damaged roots or plant material where practical. Severely affected plants may need to be removed. Treatment should be based on correct diagnosis of the causal organism.','Use well-drained soil, avoid overwatering, prevent standing water, use clean planting material, and remove severely infected plants or roots.','High','University of Maryland Extension - Root Rots: https://extension.umd.edu/resource/root-rots-indoor-plants ; Penn State Extension - Fungal Root Rots: https://extension.psu.edu/fungal-root-rots-and-chemical-fungicide-use','2026-09-26 16:40:58','2026-09-26 16:57:32'),(5,'Anthracnose','Fungal','Anthracnose is a group of fungal diseases that can affect leaves, stems, shoots, flowers, and fruits depending on the host plant and pathogen.','Caused by several fungal pathogens, commonly including species of Colletotrichum and related fungi. Warm, moist conditions can encourage disease development and spread.','Symptoms vary by host but can include brown, tan, reddish, or black leaf spots, sunken lesions on stems or fruits, dead tissue, premature leaf drop, and dieback of infected shoots.','Remove and destroy infected plant material. Improve air circulation and avoid working with plants when foliage is wet. Where appropriate, registered fungicides may be used according to the label and the specific host.','Use healthy planting material, remove infected debris, avoid unnecessary overhead irrigation, maintain good air circulation, and sanitize tools after working with infected plants.','Medium','University of Minnesota Extension - Anthracnose: https://extension.umn.edu/agriculture/specialty-crops/vegetable-farming/disease-management/anthracnose-of-cucurbits ; Penn State Extension - Anthracnose of Brambles: https://extension.psu.edu/anthracnose-in-home-plantings-of-brambles','2026-09-26 16:40:58','2026-09-26 16:57:32'),(6,'Downy Mildew','Oomycete','Downy mildew is a group of plant diseases caused by oomycete pathogens. It can produce yellow or pale leaf spots and characteristic downy growth on the underside of leaves under humid conditions.','Caused by oomycete pathogens including species of Peronospora, Plasmopara, Pseudoperonospora, and Bremia. Cool, humid, and wet conditions can favor infection.','Pale green or yellow angular spots develop on the upper leaf surface. Under humid conditions, gray, white, or purplish downy growth may appear on the underside of leaves. Infected leaves can yellow, brown, wilt, and die.','Remove infected plant material where practical, improve air circulation, and reduce periods of leaf wetness. For susceptible crops, appropriate fungicide or oomycete-management products may be used according to the label and host plant.','Avoid overcrowding, improve air circulation, reduce prolonged leaf wetness, use drip or ground-level irrigation when possible, and remove infected plant debris.','High','Penn State Extension - Downy Mildew: https://extension.psu.edu/downy-mildew ; NC State Extension - Downy Mildew: https://content.ces.ncsu.edu/downy-mildew-of-bedding-plants ; University of Maryland Extension - Downy Mildew: https://www.extension.umd.edu/resource/downy-mildew-flowers','2026-09-26 16:40:58','2026-09-26 16:57:32'),(7,'Blight','Fungal / Bacterial','Blight is a general plant disease term describing rapid browning, death, or decay of leaves, shoots, stems, flowers, or other plant tissues. Different types of blight have different causes.','Depending on the type of blight, causes can include fungal, oomycete, or bacterial pathogens. The exact causal organism must be determined for accurate diagnosis and treatment.','Water-soaked or discolored spots may develop and enlarge rapidly. Leaves, shoots, stems, flowers, or fruits may turn brown or black and die. Severe infections can result in extensive tissue death and plant decline.','Remove and destroy severely infected plant material. Improve air circulation and reduce leaf wetness. Avoid spreading the pathogen through contaminated tools, water, or plant debris. Specific treatment depends on the type of blight and causal pathogen.','Use healthy planting material, maintain good spacing and air circulation, avoid unnecessary overhead watering, remove infected plant debris, and sanitize tools between infected and healthy plants.','High','Penn State Extension - Diagnosing Common Plant Problems: https://extension.psu.edu/diagnosing-common-problems-in-the-vegetable-garden ; University of Minnesota Extension - Managing Plant Diseases: https://extension.umn.edu/garden-and-home/yard-and-garden/yard-and-garden-problems/managing-plant-diseases-in-the-home-garden','2026-09-26 16:40:58','2026-09-26 16:57:32');
/*!40000 ALTER TABLE `diseases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `model_versions`
--

DROP TABLE IF EXISTS `model_versions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `model_versions` (
  `model_version_id` int NOT NULL AUTO_INCREMENT,
  `model_name` varchar(150) NOT NULL,
  `version` varchar(50) NOT NULL,
  `model_file` varchar(500) DEFAULT NULL,
  `accuracy` decimal(5,2) DEFAULT NULL,
  `precision_score` decimal(5,2) DEFAULT NULL,
  `recall_score` decimal(5,2) DEFAULT NULL,
  `f1_score` decimal(5,2) DEFAULT NULL,
  `dataset_description` text,
  `training_date` date DEFAULT NULL,
  `notes` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`model_version_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `model_versions`
--

LOCK TABLES `model_versions` WRITE;
/*!40000 ALTER TABLE `model_versions` DISABLE KEYS */;
INSERT INTO `model_versions` VALUES (1,'Himalayan Plant Disease Classification Model','1.0','models/himalayan_plant_disease_v1.keras',NULL,NULL,NULL,NULL,'Image dataset containing selected Himalayan plants and their associated diseases.',NULL,'Initial model version.','2026-09-26 16:41:16');
/*!40000 ALTER TABLE `model_versions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plant_diseases`
--

DROP TABLE IF EXISTS `plant_diseases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plant_diseases` (
  `relationship_id` int NOT NULL AUTO_INCREMENT,
  `plant_id` int NOT NULL,
  `disease_id` int NOT NULL,
  `notes` text,
  PRIMARY KEY (`relationship_id`),
  UNIQUE KEY `plant_id` (`plant_id`,`disease_id`),
  KEY `disease_id` (`disease_id`),
  CONSTRAINT `plant_diseases_ibfk_1` FOREIGN KEY (`plant_id`) REFERENCES `plants` (`plant_id`) ON DELETE CASCADE,
  CONSTRAINT `plant_diseases_ibfk_2` FOREIGN KEY (`disease_id`) REFERENCES `diseases` (`disease_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plant_diseases`
--

LOCK TABLES `plant_diseases` WRITE;
/*!40000 ALTER TABLE `plant_diseases` DISABLE KEYS */;
INSERT INTO `plant_diseases` VALUES (1,1,1,'Leaf spot has been documented on Rhododendron arboreum in Nepal.'),(2,1,2,'Powdery mildew is reported as a common disease of Rhododendron.'),(3,1,3,'Rust is a documented disease affecting Rhododendron species.'),(4,2,1,'Round leaf spot disease has been documented on Zanthoxylum armatum.'),(5,2,3,'Leaf rust has been documented on Zanthoxylum armatum.'),(6,7,2,'Vaccinium glaucoalbum is reported as susceptible to powdery mildew.'),(7,7,4,'Vaccinium glaucoalbum is reported as susceptible to root rot.'),(8,8,2,'Powdery mildew has been documented on Alnus nepalensis in a Nepal forest pathogen survey.'),(9,8,4,'Root and collar rot caused by Phytophthora species is documented in alder; verify the exact pathogen for Alnus nepalensis before using this as a species-specific diagnosis.'),(10,9,4,'Root rot/damping-off has been documented in Pinus roxburghii nurseries.'),(11,9,7,'Needle blight/needle cast diseases are documented on Pinus roxburghii.'),(12,10,3,'Stem/needle rust has been documented on Pinus wallichiana.'),(13,10,4,'Root rot has been recorded on Pinus wallichiana.'),(14,10,7,'Needle blight caused by Lophodermium species has been documented on Pinus wallichiana.'),(15,11,4,'Root rot is documented among diseases affecting Juniper species.'),(16,11,7,'Twig and foliage blight diseases are documented among Juniper species.'),(17,11,3,'Rust diseases are documented among Juniper species.'),(18,12,2,'Quercus semecarpifolia is reported as susceptible to powdery mildew.'),(19,13,5,'Anthracnose is reported among diseases associated with Acer oblongum.'),(20,13,4,'Phytophthora and Armillaria root rots are reported among diseases associated with Acer oblongum.'),(21,14,4,'Root rot is listed among diseases affecting cultivated Nardostachys jatamansi.'),(22,14,1,'Brown/leaf spot is listed among diseases affecting cultivated Nardostachys jatamansi.'),(23,15,1,'Alternaria, Curvularia, and other leaf spot diseases have been documented on Swertia chirayita in Nepal.'),(24,15,7,'Colletotrichum leaf blight has been documented on Swertia chirayita in Nepal.'),(25,15,4,'Fusarium and Rhizoctonia-associated root diseases have been documented on Swertia chirayita.');
/*!40000 ALTER TABLE `plant_diseases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plants`
--

DROP TABLE IF EXISTS `plants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plants` (
  `plant_id` int NOT NULL AUTO_INCREMENT,
  `plant_name` varchar(150) NOT NULL,
  `scientific_name` varchar(200) DEFAULT NULL,
  `local_name` varchar(150) DEFAULT NULL,
  `organism_type` enum('Plant','Fungus') DEFAULT 'Plant',
  `life_form` enum('Tree','Shrub','Herb','Fungus') DEFAULT 'Herb',
  `is_medicinal` enum('Yes','No') DEFAULT 'No',
  `description` text,
  `habitat` text,
  `altitude_range` varchar(100) DEFAULT NULL,
  `uses` text,
  `image_path` varchar(500) DEFAULT NULL,
  `status` enum('Active','Inactive') DEFAULT 'Active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`plant_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plants`
--

LOCK TABLES `plants` WRITE;
/*!40000 ALTER TABLE `plants` DISABLE KEYS */;
INSERT INTO `plants` VALUES (1,'Rhododendron','Rhododendron arboreum Sm.','Laliguras (लालीगुराँस)','Plant','Tree','Yes','Rhododendron arboreum is an evergreen Himalayan tree and the national flower of Nepal. It produces clusters of bright red, pink, or white flowers and is commonly found in mountain forests.','Mountain forests, temperate forests, and forest margins of the Himalayas.','1500–3600 m','Flowers are used traditionally as food and for beverages. The plant also has traditional medicinal uses and is important culturally and environmentally in Nepal.',NULL,'Active','2026-09-26 16:39:33','2026-09-26 16:51:11'),(2,'Timur','Zanthoxylum armatum DC.','Timur (टिमुर)','Plant','Shrub','Yes','Timur is a spiny aromatic shrub or small tree native to the Himalayan region. Its fruits have a characteristic spicy and citrus-like flavor.','Open places, forest undergrowth, and subtropical to temperate Himalayan areas.','1000–2500 m','Fruits and seeds are widely used as a spice and traditional medicine. Different plant parts have been traditionally used for digestive problems, toothache, fever, and other conditions.',NULL,'Active','2026-09-26 16:39:33','2026-09-26 16:51:11'),(3,'Kutki','Neopicrorhiza scrophulariiflora (Pennell) D.Y.Hong','Kutki (कुटकी)','Plant','Herb','Yes','Kutki is a small perennial Himalayan medicinal herb with a short rhizome and basal leaves. It is an important high-altitude medicinal plant.','Alpine and subalpine grasslands, rocky slopes, and moist Himalayan habitats.','3500–4800 m','The rhizome is traditionally used in herbal medicine and is an important medicinal plant collected and traded in Himalayan regions.',NULL,'Active','2026-09-26 16:39:33','2026-09-26 16:51:11'),(4,'Yarsagumba','Ophiocordyceps sinensis (Berk.) G.H.Sung et al.','Yarsagumba (यार्सागुम्बा)','Fungus','Fungus','Yes','Yarsagumba is a parasitic fungus associated with insect larvae in high-altitude Himalayan grasslands. It is not a true plant and is included in this project as a Himalayan medicinal organism.','High-altitude alpine meadows and grasslands of the Himalayan region.','3000–5000 m','Traditionally collected and used in Himalayan and Tibetan medicinal practices. It is also an important non-timber forest product.',NULL,'Active','2026-09-26 16:39:33','2026-09-26 16:51:11'),(5,'Atis','Aconitum heterophyllum Wall. ex Royle','Atis / Ativisha (अतीस)','Plant','Herb','Yes','Atis is a perennial Himalayan medicinal herb belonging to the buttercup family. It is found mainly in subalpine and alpine regions.','Subalpine and alpine grasslands and mountain slopes.','3000–4500 m','The tuberous roots have been traditionally used in Himalayan and Ayurvedic medicine. It is an important medicinal plant in Nepal.',NULL,'Active','2026-09-26 16:39:33','2026-09-26 16:51:11'),(6,'Himalayan Raspberry','Rubus ellipticus Sm.','Ainselu (ऐँसेलु)','Plant','Shrub','No','Himalayan raspberry is a thorny shrub that produces small yellow to golden edible berries. It is common in hilly areas of Nepal.','Open areas, forest margins, disturbed land, and hilly Himalayan regions.','Approximately 1000–2500 m','The edible fruits are consumed fresh and may be used for traditional food products. The plant also contributes to local biodiversity and wildlife food resources.',NULL,'Active','2026-09-26 16:39:33','2026-09-26 16:54:56'),(7,'Himalayan Blueberry','Vaccinium glaucoalbum Hook.f. ex C.B.Clarke','Nilo Ainselu (निलो ऐँसेलु)','Plant','Shrub','No','Himalayan blueberry is an evergreen shrub producing dark bluish-black edible berries. It is associated with high-altitude Himalayan forests and thickets.','High-altitude temperate forests, thickets, and forest margins of the eastern Himalayas.','2600–3300 m','The berries are edible and are locally collected as a wild fruit. The plant is also valued for its ornamental foliage and ecological importance.',NULL,'Active','2026-09-26 16:39:33','2026-09-26 16:54:56'),(8,'Alder','Alnus nepalensis D.Don','Utis (उत्तिस)','Plant','Tree','No','Nepalese alder is a fast-growing deciduous tree important in Himalayan forests and agroforestry systems. It can improve soil fertility through nitrogen fixation.','Stream banks, ravines, moist forests, slopes, and disturbed areas in the Himalayan foothills.','500–3000 m','Used for fuelwood, charcoal, light construction, boxes, furniture parts, and erosion control. It is also planted for land restoration and agroforestry.',NULL,'Active','2026-09-26 16:39:33','2026-09-26 16:54:56'),(9,'Chir Pine','Pinus roxburghii Sarg.','Khote Salla / Rani Salla (खोटे सल्ला)','Plant','Tree','No','Chir pine is a tall evergreen conifer with long needles growing in groups of three. It is one of the characteristic pine species of the lower Himalayan region.','Dry slopes, foothills, outer valleys, and temperate Himalayan forests.','500–2700 m','Wood is used for construction and furniture, while resin is collected for industrial products. The species is also important for forestry and ecosystem services.',NULL,'Active','2026-09-26 16:39:33','2026-09-26 16:54:56'),(10,'Blue Pine','Pinus wallichiana A.B.Jacks.','Gobre Salla (गोब्रे सल्ला)','Plant','Tree','No','Blue pine is a tall evergreen Himalayan conifer with long blue-green needles. It is an important tree of mountain forests.','Mountain valleys, slopes, river basins, and temperate Himalayan forests.','1000–3300 m','The wood is used for construction and other timber purposes. Resin and other forest products may also be obtained from the tree.',NULL,'Active','2026-09-26 16:39:33','2026-09-26 16:54:56'),(11,'Juniper','Juniperus indica Bertol.','Dhupi (धुपी)','Plant','Tree','Yes','Black juniper is a Himalayan evergreen conifer that may grow as a shrub or small tree. It is particularly important in high-altitude Himalayan ecosystems and cultural practices.','Mountain slopes, high-altitude forests, thickets, and rocky Himalayan areas.','2600–5100 m','Leaves and twigs are traditionally burned as incense. Different plant parts have also been used traditionally in herbal medicine. Wood is used for poles and fuelwood.',NULL,'Active','2026-09-26 16:39:33','2026-09-26 16:51:11'),(12,'Himalayan Oak','Quercus semecarpifolia Sm.','Khasru (खस्रु)','Plant','Tree','No','Himalayan oak is an evergreen oak tree characteristic of upper temperate and subalpine Himalayan forests. It is an important forest species for soil and ecosystem stability.','Moist temperate and subalpine forests, mountain ridges, and slopes.','1700–3800 m','Provides fuelwood, fodder, leaf litter, and timber. It is also important for watershed protection, soil conservation, and Himalayan forest ecosystems.',NULL,'Active','2026-09-26 16:39:33','2026-09-26 16:54:56'),(13,'Himalayan Maple','Acer oblongum Wall. ex DC.','Phirphire (फिरफिरे)','Plant','Tree','No','Himalayan maple is a medium-sized evergreen or semi-deciduous tree found in moist Himalayan forests. It has distinctive oblong leaves and winged fruits.','Moist forests, lower Himalayan foothills, and areas near streams.','600–2000 m','Used for wood products including planks, boxes, plywood, agricultural implements, and household items. It is also planted as an ornamental tree.',NULL,'Active','2026-09-26 16:39:33','2026-09-26 16:54:56'),(14,'Jatamasi','Nardostachys jatamansi (D.Don) DC.','Jatamasi (जटामसी)','Plant','Herb','Yes','Jatamasi is a perennial aromatic Himalayan medicinal herb with a valuable rhizome. It grows mainly in high-altitude mountain environments.','Subalpine and alpine grasslands, moist mountain slopes, and high-altitude Himalayan habitats.','3200–5000 m','The aromatic rhizome is traditionally used in herbal medicine and for its fragrance. It is also used in incense and traditional preparations.',NULL,'Active','2026-09-26 16:39:33','2026-09-26 16:51:11'),(15,'Chiraito','Swertia chirayita (Roxb.) H.Karst.','Chiraito (चिराइतो)','Plant','Herb','Yes','Chiraito is a bitter medicinal herb native to the Himalayan region. It is an important traditional medicinal plant of Nepal.','Temperate mountain areas, forest margins, grasslands, and open slopes.','1500–2500 m','The whole plant is traditionally used in herbal medicine, especially in preparations associated with fever and digestive complaints.',NULL,'Active','2026-09-26 16:39:33','2026-09-26 16:51:11');
/*!40000 ALTER TABLE `plants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `predictions`
--

DROP TABLE IF EXISTS `predictions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `predictions` (
  `prediction_id` int NOT NULL AUTO_INCREMENT,
  `plant_id` int DEFAULT NULL,
  `disease_id` int DEFAULT NULL,
  `model_version_id` int DEFAULT NULL,
  `image_path` varchar(500) DEFAULT NULL,
  `confidence` decimal(5,2) DEFAULT NULL,
  `predicted_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`prediction_id`),
  KEY `plant_id` (`plant_id`),
  KEY `disease_id` (`disease_id`),
  KEY `model_version_id` (`model_version_id`),
  CONSTRAINT `predictions_ibfk_1` FOREIGN KEY (`plant_id`) REFERENCES `plants` (`plant_id`) ON DELETE SET NULL,
  CONSTRAINT `predictions_ibfk_2` FOREIGN KEY (`disease_id`) REFERENCES `diseases` (`disease_id`) ON DELETE SET NULL,
  CONSTRAINT `predictions_ibfk_3` FOREIGN KEY (`model_version_id`) REFERENCES `model_versions` (`model_version_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `predictions`
--

LOCK TABLES `predictions` WRITE;
/*!40000 ALTER TABLE `predictions` DISABLE KEYS */;
/*!40000 ALTER TABLE `predictions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-27 19:33:49
