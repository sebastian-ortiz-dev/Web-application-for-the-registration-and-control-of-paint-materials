--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2026-05-11 14:14:38

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

CREATE Schema IF not exists public;

set search_path to  public;

GRANT ALL ON SCHEMA public TO public;

--
-- TOC entry 226 (class 1259 OID 16447)
-- Name: distribuidor; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS distribuidor (
    id_distribuidor integer NOT NULL,
    nombre character varying(255) NOT NULL,
    correo character varying(255),
    direccion character varying(500) NOT NULL,
    telefono character varying(25),
    rif character varying(50),
    borrado boolean DEFAULT false,
    fecha_registro date
);


--
-- TOC entry 225 (class 1259 OID 16446)
-- Name: Distribuidor_id_distribuidor_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE IF NOT EXISTS "Distribuidor_id_distribuidor_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4974 (class 0 OID 0)
-- Dependencies: 225
-- Name: Distribuidor_id_distribuidor_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "Distribuidor_id_distribuidor_seq" OWNED BY distribuidor.id_distribuidor;


--
-- TOC entry 224 (class 1259 OID 16435)
-- Name: movimientos_inventario; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS movimientos_inventario (
    id_movimiento bigint NOT NULL,
    id_producto integer NOT NULL,
    cantidad integer,
    fecha timestamp(0) without time zone NOT NULL,
    id_usuario integer,
    motivo character varying(500),
    tipo_movimiento integer
);


--
-- TOC entry 223 (class 1259 OID 16434)
-- Name: Movimientos_Inventario_id_movimiento_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE IF NOT EXISTS "Movimientos_Inventario_id_movimiento_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4975 (class 0 OID 0)
-- Dependencies: 223
-- Name: Movimientos_Inventario_id_movimiento_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "Movimientos_Inventario_id_movimiento_seq" OWNED BY movimientos_inventario.id_movimiento;


--
-- TOC entry 222 (class 1259 OID 16414)
-- Name: producto; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS producto (
    id_producto integer NOT NULL,
    nombre_producto character varying(255) NOT NULL,
    descripcion character varying(500),
    precio_venta numeric(10,2) NOT NULL,
    cantidad integer NOT NULL,
    fecha_actualizacion date NOT NULL,
    imagen character varying(500),
    id_distribuidor integer,
    borrado boolean DEFAULT false,
    id_categoria integer,
    id_medida integer,
    last_moviment boolean DEFAULT false,
    cantidad_minima integer
);


--
-- TOC entry 221 (class 1259 OID 16413)
-- Name: Productos_id_producto_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE IF NOT EXISTS "Productos_id_producto_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4976 (class 0 OID 0)
-- Dependencies: 221
-- Name: Productos_id_producto_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "Productos_id_producto_seq" OWNED BY producto.id_producto;


--
-- TOC entry 218 (class 1259 OID 16391)
-- Name: usuario; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS usuario (
    id_usuario integer NOT NULL,
    nombre_usuario character varying(255) NOT NULL,
    clave text NOT NULL,
    id_nivel integer NOT NULL,
    imagen_usu character varying(500),
    fecha_creacion date,
    borrado boolean DEFAULT false
);


--
-- TOC entry 217 (class 1259 OID 16390)
-- Name: Usuarios_id_usuario_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE IF NOT EXISTS "Usuarios_id_usuario_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4977 (class 0 OID 0)
-- Dependencies: 217
-- Name: Usuarios_id_usuario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "Usuarios_id_usuario_seq" OWNED BY usuario.id_usuario;


--
-- TOC entry 230 (class 1259 OID 41057)
-- Name: categorias; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS categorias (
    id_categoria integer NOT NULL,
    categoria character(350)
);


--
-- TOC entry 229 (class 1259 OID 41056)
-- Name: categorias_id_categoria_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE IF NOT EXISTS categorias_id_categoria_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4978 (class 0 OID 0)
-- Dependencies: 229
-- Name: categorias_id_categoria_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE categorias_id_categoria_seq OWNED BY categorias.id_categoria;


--
-- TOC entry 228 (class 1259 OID 32847)
-- Name: movimientos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS movimientos (
    id integer NOT NULL,
    movimiento character varying(255)
);


--
-- TOC entry 227 (class 1259 OID 32846)
-- Name: movimientos_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE IF NOT EXISTS movimientos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4979 (class 0 OID 0)
-- Dependencies: 227
-- Name: movimientos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE movimientos_id_seq OWNED BY movimientos.id;


--
-- TOC entry 220 (class 1259 OID 16402)
-- Name: niveles_acceso; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS niveles_acceso (
    id_nivel integer NOT NULL,
    nombre_nivel character varying(255) NOT NULL
);


--
-- TOC entry 219 (class 1259 OID 16401)
-- Name: niveles_acceso_id_nivel_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE IF NOT EXISTS niveles_acceso_id_nivel_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4980 (class 0 OID 0)
-- Dependencies: 219
-- Name: niveles_acceso_id_nivel_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE niveles_acceso_id_nivel_seq OWNED BY niveles_acceso.id_nivel;


--
-- TOC entry 234 (class 1259 OID 57476)
-- Name: refresh_token; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS refresh_token (
    id_refresh bigint NOT NULL,
    id_usuario bigint NOT NULL,
    uuid character varying(1000) NOT NULL,
    is_revoked boolean DEFAULT false NOT NULL,
    date_expired date NOT NULL
);


--
-- TOC entry 233 (class 1259 OID 57475)
-- Name: refresh_token _id_refresh_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE IF NOT EXISTS "refresh_token _id_refresh_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4981 (class 0 OID 0)
-- Dependencies: 233
-- Name: refresh_token _id_refresh_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "refresh_token _id_refresh_seq" OWNED BY refresh_token.id_refresh;


--
-- TOC entry 232 (class 1259 OID 41069)
-- Name: unidad_medida; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE IF NOT EXISTS unidad_medida (
    id_medida integer NOT NULL,
    medida character(50)
);


--
-- TOC entry 231 (class 1259 OID 41068)
-- Name: unidad_medida_id_medida_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE IF NOT EXISTS unidad_medida_id_medida_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4982 (class 0 OID 0)
-- Dependencies: 231
-- Name: unidad_medida_id_medida_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE unidad_medida_id_medida_seq OWNED BY unidad_medida.id_medida;


--
-- TOC entry 4792 (class 2604 OID 41060)
-- Name: categorias id_categoria; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY categorias ALTER COLUMN id_categoria SET DEFAULT nextval('categorias_id_categoria_seq'::regclass);


--
-- TOC entry 4789 (class 2604 OID 16450)
-- Name: distribuidor id_distribuidor; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY distribuidor ALTER COLUMN id_distribuidor SET DEFAULT nextval('"Distribuidor_id_distribuidor_seq"'::regclass);


--
-- TOC entry 4791 (class 2604 OID 32850)
-- Name: movimientos id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY movimientos ALTER COLUMN id SET DEFAULT nextval('movimientos_id_seq'::regclass);


--
-- TOC entry 4788 (class 2604 OID 16438)
-- Name: movimientos_inventario id_movimiento; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY movimientos_inventario ALTER COLUMN id_movimiento SET DEFAULT nextval('"Movimientos_Inventario_id_movimiento_seq"'::regclass);


--
-- TOC entry 4784 (class 2604 OID 16405)
-- Name: niveles_acceso id_nivel; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY niveles_acceso ALTER COLUMN id_nivel SET DEFAULT nextval('niveles_acceso_id_nivel_seq'::regclass);


--
-- TOC entry 4785 (class 2604 OID 16417)
-- Name: producto id_producto; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY producto ALTER COLUMN id_producto SET DEFAULT nextval('"Productos_id_producto_seq"'::regclass);


--
-- TOC entry 4794 (class 2604 OID 57479)
-- Name: refresh_token id_refresh; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY refresh_token ALTER COLUMN id_refresh SET DEFAULT nextval('"refresh_token _id_refresh_seq"'::regclass);


--
-- TOC entry 4793 (class 2604 OID 41072)
-- Name: unidad_medida id_medida; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY unidad_medida ALTER COLUMN id_medida SET DEFAULT nextval('unidad_medida_id_medida_seq'::regclass);


--
-- TOC entry 4782 (class 2604 OID 16394)
-- Name: usuario id_usuario; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY usuario ALTER COLUMN id_usuario SET DEFAULT nextval('"Usuarios_id_usuario_seq"'::regclass);


--
-- TOC entry 4806 (class 2606 OID 16454)
-- Name: distribuidor Distribuidor_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY distribuidor
    ADD CONSTRAINT "Distribuidor_pkey" PRIMARY KEY (id_distribuidor);


--
-- TOC entry 4804 (class 2606 OID 16440)
-- Name: movimientos_inventario Movimientos_Inventario_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY movimientos_inventario
    ADD CONSTRAINT "Movimientos_Inventario_pkey" PRIMARY KEY (id_movimiento);


--
-- TOC entry 4802 (class 2606 OID 16421)
-- Name: producto Productos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY producto
    ADD CONSTRAINT "Productos_pkey" PRIMARY KEY (id_producto);


--
-- TOC entry 4797 (class 2606 OID 16398)
-- Name: usuario Usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY usuario
    ADD CONSTRAINT "Usuarios_pkey" PRIMARY KEY (id_usuario);


--
-- TOC entry 4810 (class 2606 OID 41062)
-- Name: categorias categorias_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY categorias
    ADD CONSTRAINT categorias_pkey PRIMARY KEY (id_categoria);


--
-- TOC entry 4808 (class 2606 OID 32852)
-- Name: movimientos movimientos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY movimientos
    ADD CONSTRAINT movimientos_pkey PRIMARY KEY (id);


--
-- TOC entry 4800 (class 2606 OID 16407)
-- Name: niveles_acceso niveles_acceso_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY niveles_acceso
    ADD CONSTRAINT niveles_acceso_pkey PRIMARY KEY (id_nivel);


--
-- TOC entry 4814 (class 2606 OID 57483)
-- Name: refresh_token primary_refresh; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY refresh_token
    ADD CONSTRAINT primary_refresh PRIMARY KEY (id_refresh);


--
-- TOC entry 4812 (class 2606 OID 41074)
-- Name: unidad_medida unidad_medida_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY unidad_medida
    ADD CONSTRAINT unidad_medida_pkey PRIMARY KEY (id_medida);


--
-- TOC entry 4816 (class 2606 OID 57485)
-- Name: refresh_token unique_uuid; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY refresh_token
    ADD CONSTRAINT unique_uuid UNIQUE (uuid) INCLUDE (uuid);


--
-- TOC entry 4798 (class 1259 OID 32865)
-- Name: indx_usuario_name; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX indx_usuario_name ON usuario USING btree (nombre_usuario) WHERE (borrado = false);


--
-- TOC entry 4823 (class 2606 OID 57486)
-- Name: refresh_token fk_id_user; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY refresh_token
    ADD CONSTRAINT fk_id_user FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario);


--
-- TOC entry 4820 (class 2606 OID 16441)
-- Name: movimientos_inventario fk_movimiento_producto; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY movimientos_inventario
    ADD CONSTRAINT fk_movimiento_producto FOREIGN KEY (id_producto) REFERENCES producto(id_producto);


--
-- TOC entry 4821 (class 2606 OID 24652)
-- Name: movimientos_inventario fk_movimiento_usuario; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY movimientos_inventario
    ADD CONSTRAINT fk_movimiento_usuario FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) NOT VALID;


--
-- TOC entry 4818 (class 2606 OID 41063)
-- Name: producto fk_producto_categoria; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY producto
    ADD CONSTRAINT fk_producto_categoria FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria) NOT VALID;


--
-- TOC entry 4819 (class 2606 OID 24647)
-- Name: producto fk_producto_distribuidor; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY producto
    ADD CONSTRAINT fk_producto_distribuidor FOREIGN KEY (id_distribuidor) REFERENCES distribuidor(id_distribuidor) NOT VALID;


--
-- TOC entry 4822 (class 2606 OID 32853)
-- Name: movimientos_inventario fk_tipo_movimiento; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY movimientos_inventario
    ADD CONSTRAINT fk_tipo_movimiento FOREIGN KEY (tipo_movimiento) REFERENCES movimientos(id) NOT VALID;


--
-- TOC entry 4817 (class 2606 OID 16408)
-- Name: usuario fk_usuario_nivel; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY usuario
    ADD CONSTRAINT fk_usuario_nivel FOREIGN KEY (id_nivel) REFERENCES niveles_acceso(id_nivel) NOT VALID;

INSERT INTO niveles_acceso (nombre_nivel) VALUES ('Administrador');

INSERT INTO niveles_acceso (nombre_nivel) VALUES ('Trabajador');

INSERT INTO movimientos (movimiento) VALUES ('Entrada');

INSERT INTO movimientos (movimiento) VALUES ('Salida');

INSERT INTO movimientos (movimiento) VALUES ('Devolucion');

INSERT INTO movimientos (movimiento) VALUES ('Ajuste');

INSERT INTO unidad_medida (medida) VALUES ('Galon');

INSERT INTO categorias (categoria) VALUES ('Pinturas y recubrimientos');

INSERT INTO usuario (nombre_usuario, clave, id_nivel, imagen_usu, fecha_creacion) VALUES ('admin', '$argon2id$v=19$m=65536,t=3,p=4$f2kkd1t6h1nYMRI6XNT6KQ$1ogddX5jZbDWA1W3PiOfphLIltaywzNDxYo5yyx/3Oc', 1, 'usuario_defecto.png', '2026-04-20') ON CONFLICT (nombre_usuario) WHERE borrado = FALSE DO NOTHING;

INSERT INTO distribuidor (nombre, correo, direccion, telefono, rif, borrado, fecha_registro) VALUES ('proveedor', 'proveedor@gmail.com', 'San antonio de los altos', '0414-325-56-77', 'j-555656535', 'False', '2026-04-20');

INSERT INTO producto (nombre_producto, descripcion, precio_venta, cantidad, fecha_actualizacion, imagen, id_distribuidor, borrado, id_categoria, id_medida, cantidad_minima) VALUES ('pintura roja', 'pintura roja', 20, 30, '2026-04-20', 'pintura.jpg', 1, 'False', 1, 1, 5);

INSERT INTO movimientos_inventario (id_producto, cantidad, fecha, id_usuario, motivo, tipo_movimiento) VALUES (1, 30, '2026-04-20', 1, 'Entrada de nuevo producto', 1)

-- Completed on 2026-05-11 14:14:39

--
-- PostgreSQL database dump complete
--

