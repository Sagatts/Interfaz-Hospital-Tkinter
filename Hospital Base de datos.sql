-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 24-07-2023 a las 04:47:47
-- Versión del servidor: 8.0.17
-- Versión de PHP: 7.3.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `hospital`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cuentas`
--

CREATE TABLE `cuentas` (
  `Usuario` varchar(200) NOT NULL,
  `Contraseña` varchar(200) NOT NULL,
  `Correo` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `cuentas`
--

INSERT INTO `cuentas` (`Usuario`, `Contraseña`, `Correo`) VALUES
('Arriagada', 'Arriagada', 'fernandoarriagada123455@gmail.com'),
('Fernando', 'Arriagada', 'fernandomike2004@hotmail.com'),
('FernandoMike', 'ArriagadaTrujillo', 'fernandotrujillo123455@gmail.com'),
('Mike', 'Trujillo', 'fernando.arriagada.22@alumnos.uda.cl'),
('Nicolas', 'Contreras', 'nicolas.contreras.22@alumnos.uda.cl'),
('qwert', 'qwert', 'fernandomike2004@hotmail.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `fondos`
--

CREATE TABLE `fondos` (
  `id` int(50) NOT NULL,
  `Fondos` int(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `fondos`
--

INSERT INTO `fondos` (`id`, `Fondos`) VALUES
(1, 98254525);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pacientes`
--

CREATE TABLE `pacientes` (
  `Rut` varchar(50) NOT NULL,
  `Nombre` varchar(200) NOT NULL,
  `Fecha_de_ingreso` date NOT NULL,
  `Tipo_de_prevision` varchar(200) NOT NULL,
  `Motivo_de_ingreso` varchar(200) NOT NULL,
  `Derivacion` varchar(200) NOT NULL,
  `Box` varchar(50) DEFAULT NULL,
  `Medico_y_Especialidad` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `pacientes`
--

INSERT INTO `pacientes` (`Rut`, `Nombre`, `Fecha_de_ingreso`, `Tipo_de_prevision`, `Motivo_de_ingreso`, `Derivacion`, `Box`, `Medico_y_Especialidad`) VALUES
('21360024-9', 'Miguel', '2020-08-19', 'Isapre', 'Fractura', 'Urgencia', '2', ''),
('21464913-6', 'Sebastian', '2019-08-28', 'Isapre', 'Dolor de pie', 'Consulta medica', '', '(\'Fernando\', \'Cardiologia\')');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pago_pacientes`
--

CREATE TABLE `pago_pacientes` (
  `Rut` varchar(50) NOT NULL,
  `Nombre` varchar(200) NOT NULL,
  `Tipo_de_prevision` varchar(200) NOT NULL,
  `Derivacion` varchar(200) NOT NULL,
  `Hospitalizacion` varchar(200) NOT NULL,
  `Dias_en_cama` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Dinero_a_pagar` int(200) NOT NULL,
  `Pagado` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `pago_pacientes`
--

INSERT INTO `pago_pacientes` (`Rut`, `Nombre`, `Tipo_de_prevision`, `Derivacion`, `Hospitalizacion`, `Dias_en_cama`, `Dinero_a_pagar`, `Pagado`) VALUES
('21360024-9', 'Miguel', 'Isapre', 'Urgencia', 'Si', '4', 135000, 'No'),
('21464913-6', 'Sebastian', 'Isapre', 'Consulta medica', 'No', '0', 20000, 'No');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pago_personal`
--

CREATE TABLE `pago_personal` (
  `Rut` varchar(50) NOT NULL,
  `Nombre` varchar(200) NOT NULL,
  `Fecha_de_ingreso` date NOT NULL,
  `Sueldo_liquido` int(200) NOT NULL,
  `Pagado` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `pago_personal`
--

INSERT INTO `pago_personal` (`Rut`, `Nombre`, `Fecha_de_ingreso`, `Sueldo_liquido`, `Pagado`) VALUES
('21360024-9', 'Miguel', '2017-10-24', 2204200, 'No'),
('21436953-2', 'Matias', '2014-08-03', 1713758, 'No'),
('21507579-6', 'Fernando', '2000-01-01', 1891725, 'Si');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `personal_administrativo`
--

CREATE TABLE `personal_administrativo` (
  `Rut` varchar(50) NOT NULL,
  `Nombre` varchar(200) NOT NULL,
  `Fecha_de_ingreso` date NOT NULL,
  `Tipo_de_prevision` varchar(200) NOT NULL,
  `Sueldo_bruto` int(200) NOT NULL,
  `Rol` varchar(200) NOT NULL,
  `Unidad_administrativa` varchar(200) NOT NULL,
  `Afp` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `personal_administrativo`
--

INSERT INTO `personal_administrativo` (`Rut`, `Nombre`, `Fecha_de_ingreso`, `Tipo_de_prevision`, `Sueldo_bruto`, `Rol`, `Unidad_administrativa`, `Afp`) VALUES
('21360024-9', 'Miguel', '2017-10-24', 'Fonasa', 2140000, 'Administrativo', 'Unidad de servicios generales', 'No');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `personal_medico`
--

CREATE TABLE `personal_medico` (
  `Rut` varchar(50) NOT NULL,
  `Nombre` varchar(200) NOT NULL,
  `Fecha_de_ingreso` date NOT NULL,
  `Tipo_de_prevision` varchar(200) NOT NULL,
  `Sueldo_bruto` int(200) NOT NULL,
  `Rol` varchar(200) NOT NULL,
  `Especialidad_o_Area` varchar(200) NOT NULL,
  `Afp` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `personal_medico`
--

INSERT INTO `personal_medico` (`Rut`, `Nombre`, `Fecha_de_ingreso`, `Tipo_de_prevision`, `Sueldo_bruto`, `Rol`, `Especialidad_o_Area`, `Afp`) VALUES
('21436953-2', 'Matias', '2014-08-03', 'Fonasa', 1950000, 'Medico', 'Cardiologia', 'Si'),
('21507579-6', 'Fernando', '2000-01-01', 'Fonasa', 2050000, 'Medico', 'Cardiologia', 'Si');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cuentas`
--
ALTER TABLE `cuentas`
  ADD PRIMARY KEY (`Usuario`);

--
-- Indices de la tabla `fondos`
--
ALTER TABLE `fondos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `pacientes`
--
ALTER TABLE `pacientes`
  ADD PRIMARY KEY (`Rut`);

--
-- Indices de la tabla `pago_pacientes`
--
ALTER TABLE `pago_pacientes`
  ADD PRIMARY KEY (`Rut`);

--
-- Indices de la tabla `pago_personal`
--
ALTER TABLE `pago_personal`
  ADD PRIMARY KEY (`Rut`);

--
-- Indices de la tabla `personal_administrativo`
--
ALTER TABLE `personal_administrativo`
  ADD PRIMARY KEY (`Rut`);

--
-- Indices de la tabla `personal_medico`
--
ALTER TABLE `personal_medico`
  ADD PRIMARY KEY (`Rut`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
