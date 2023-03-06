-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema rasdb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema rasdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `rasdb` DEFAULT CHARACTER SET utf8 ;
USE `rasdb` ;

-- -----------------------------------------------------
-- Table `rasdb`.`Aposta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rasdb`.`Aposta` (
  `id` INT NOT NULL,
  `sport` VARCHAR(45) NOT NULL,
  `home_team` VARCHAR(45) NULL DEFAULT NULL,
  `away_team` VARCHAR(45) NULL DEFAULT NULL,
  `odd_home` DOUBLE NULL DEFAULT NULL,
  `odd_tie` DOUBLE NULL DEFAULT NULL,
  `odd_away` DOUBLE NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `rasdb`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rasdb`.`User` (
  `mail` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`mail`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `rasdb`.`ApostaUser`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rasdb`.`ApostaUser` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `result` VARCHAR(45) NOT NULL,
  `amount` INT NOT NULL,
  `Aposta_id` INT NOT NULL,
  `User_mail` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_ApostaUser_Aposta_idx` (`Aposta_id` ASC) VISIBLE,
  INDEX `fk_ApostaUser_User1_idx` (`User_mail` ASC) VISIBLE,
  CONSTRAINT `fk_ApostaUser_Aposta`
    FOREIGN KEY (`Aposta_id`)
    REFERENCES `rasdb`.`Aposta` (`id`),
  CONSTRAINT `fk_ApostaUser_User1`
    FOREIGN KEY (`User_mail`)
    REFERENCES `rasdb`.`User` (`mail`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `rasdb`.`DriverOdds`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rasdb`.`DriverOdds` (
  `driver` VARCHAR(45) NOT NULL,
  `odd` DOUBLE NOT NULL,
  `Aposta_id` INT NOT NULL,
  PRIMARY KEY (`driver`, `Aposta_id`),
  INDEX `fk_DriverOdds_Aposta1_idx` (`Aposta_id` ASC) VISIBLE,
  CONSTRAINT `fk_DriverOdds_Aposta1`
    FOREIGN KEY (`Aposta_id`)
    REFERENCES `rasdb`.`Aposta` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `rasdb`.`CreditosUser`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `rasdb`.`CreditosUser` (
  `moeda` VARCHAR(45) NOT NULL,
  `creditos` DOUBLE NOT NULL,
  `User_mail` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`moeda`, `User_mail`),
  INDEX `fk_CreditosUser_User1_idx` (`User_mail` ASC) VISIBLE,
  CONSTRAINT `fk_CreditosUser_User1`
    FOREIGN KEY (`User_mail`)
    REFERENCES `rasdb`.`User` (`mail`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
