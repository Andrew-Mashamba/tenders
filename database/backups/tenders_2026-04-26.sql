--
-- PostgreSQL database dump
--

\restrict bgONmQHEKpYVk6l3dmh5SAy49qNszaahWO9IGgKYuGf6SwpVLaLDTqKawFkmljq

-- Dumped from database version 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: plans; Type: TABLE; Schema: public; Owner: tenders
--

CREATE TABLE public.plans (
    id character varying NOT NULL,
    name character varying NOT NULL,
    price_monthly integer NOT NULL,
    stripe_price_id character varying,
    max_institutions integer NOT NULL,
    max_applications_per_month integer NOT NULL,
    can_download_documents boolean,
    can_control_scraper boolean,
    has_api_access boolean,
    has_email_alerts boolean
);


ALTER TABLE public.plans OWNER TO tenders;

--
-- Name: refresh_tokens; Type: TABLE; Schema: public; Owner: tenders
--

CREATE TABLE public.refresh_tokens (
    id integer NOT NULL,
    user_id integer NOT NULL,
    token_hash character varying NOT NULL,
    expires_at timestamp without time zone NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.refresh_tokens OWNER TO tenders;

--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: tenders
--

CREATE SEQUENCE public.refresh_tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.refresh_tokens_id_seq OWNER TO tenders;

--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tenders
--

ALTER SEQUENCE public.refresh_tokens_id_seq OWNED BY public.refresh_tokens.id;


--
-- Name: user_applications; Type: TABLE; Schema: public; Owner: tenders
--

CREATE TABLE public.user_applications (
    id integer NOT NULL,
    user_id integer NOT NULL,
    tender_id character varying NOT NULL,
    institution_slug character varying NOT NULL,
    status character varying,
    notes text,
    pdf_path character varying,
    submitted_at timestamp without time zone,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.user_applications OWNER TO tenders;

--
-- Name: user_applications_id_seq; Type: SEQUENCE; Schema: public; Owner: tenders
--

CREATE SEQUENCE public.user_applications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_applications_id_seq OWNER TO tenders;

--
-- Name: user_applications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tenders
--

ALTER SEQUENCE public.user_applications_id_seq OWNED BY public.user_applications.id;


--
-- Name: user_institutions; Type: TABLE; Schema: public; Owner: tenders
--

CREATE TABLE public.user_institutions (
    user_id integer NOT NULL,
    institution_slug character varying NOT NULL,
    followed_at timestamp without time zone
);


ALTER TABLE public.user_institutions OWNER TO tenders;

--
-- Name: users; Type: TABLE; Schema: public; Owner: tenders
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying NOT NULL,
    password_hash character varying NOT NULL,
    name character varying,
    company character varying,
    company_profile text,
    plan character varying,
    stripe_customer_id character varying,
    stripe_subscription_id character varying,
    subscription_status character varying,
    subscription_ends_at timestamp without time zone,
    applications_this_month integer,
    applications_reset_at timestamp without time zone,
    is_admin boolean,
    email_verified boolean,
    email_verify_token character varying,
    password_reset_token character varying,
    password_reset_expires timestamp without time zone,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.users OWNER TO tenders;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: tenders
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO tenders;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tenders
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: refresh_tokens id; Type: DEFAULT; Schema: public; Owner: tenders
--

ALTER TABLE ONLY public.refresh_tokens ALTER COLUMN id SET DEFAULT nextval('public.refresh_tokens_id_seq'::regclass);


--
-- Name: user_applications id; Type: DEFAULT; Schema: public; Owner: tenders
--

ALTER TABLE ONLY public.user_applications ALTER COLUMN id SET DEFAULT nextval('public.user_applications_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: tenders
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: plans; Type: TABLE DATA; Schema: public; Owner: tenders
--

COPY public.plans (id, name, price_monthly, stripe_price_id, max_institutions, max_applications_per_month, can_download_documents, can_control_scraper, has_api_access, has_email_alerts) FROM stdin;
free	Free	0	\N	10	5	f	f	f	f
pro	Pro	2900	\N	100	999999	t	f	f	t
enterprise	Enterprise	9900	\N	999999	999999	t	t	t	t
\.


--
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: public; Owner: tenders
--

COPY public.refresh_tokens (id, user_id, token_hash, expires_at, created_at) FROM stdin;
1	1	2ba4580ce25601f42a730201fa063e5f213352430012eb1dfdb89e626ae3d0b5	2026-05-06 09:48:14.649691	2026-04-06 09:48:14.651213
2	1	583d67e578f0c40b916d55daede79d9d8c28470e2930f77802afdeb7a0cf2459	2026-05-06 09:48:15.039418	2026-04-06 09:48:15.04011
3	1	1945f4b6af0ae727d81477e9a3920a2cce8a43d067d3b5bc2fa4e8d31a96bf35	2026-05-06 09:48:41.444681	2026-04-06 09:48:41.445402
4	1	e30a488c876c407abdea7664709493767a3488cb5df2a676cafcf429019fee44	2026-05-06 09:48:58.243072	2026-04-06 09:48:58.243716
5	2	df5492ba0d3c10f1e678ecc5136afa9392313605cb731323b0af4bd6fa404417	2026-05-21 11:29:56.235444	2026-04-21 11:29:56.23801
\.


--
-- Data for Name: user_applications; Type: TABLE DATA; Schema: public; Owner: tenders
--

COPY public.user_applications (id, user_id, tender_id, institution_slug, status, notes, pdf_path, submitted_at, created_at, updated_at) FROM stdin;
1	1	CRDB-2026-001	crdb-bank	interested	Evaluating requirements	\N	\N	2026-04-06 09:48:58.297387	2026-04-06 09:48:58.297395
\.


--
-- Data for Name: user_institutions; Type: TABLE DATA; Schema: public; Owner: tenders
--

COPY public.user_institutions (user_id, institution_slug, followed_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: tenders
--

COPY public.users (id, email, password_hash, name, company, company_profile, plan, stripe_customer_id, stripe_subscription_id, subscription_status, subscription_ends_at, applications_this_month, applications_reset_at, is_admin, email_verified, email_verify_token, password_reset_token, password_reset_expires, created_at, updated_at) FROM stdin;
1	test@tajiri.co.tz	$2b$12$SOD6FrzeYxflAhxSIMFVxOnhDJG4zsxQEaZmIruPg9.HwZ3f/b0.W	\N	\N	\N	free	\N	\N	active	\N	1	2026-04-06 09:48:14.632885	f	f	\N	\N	\N	2026-04-06 09:48:14.636752	2026-04-06 09:48:58.294647
2	pkitalima@yahoo.com	$2b$12$7GJNgPIYYlF1k5USjnSL0.MNSjkabtnkY6RwX1cYqM9t0tjKNGHX.	PETER CHARLES KITALIMA	PEAKPOINT	\N	free	\N	\N	active	\N	0	2026-04-21 11:29:56.184285	f	f	\N	\N	\N	2026-04-21 11:29:56.191876	2026-04-21 11:29:56.191883
\.


--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tenders
--

SELECT pg_catalog.setval('public.refresh_tokens_id_seq', 5, true);


--
-- Name: user_applications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tenders
--

SELECT pg_catalog.setval('public.user_applications_id_seq', 1, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tenders
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- Name: plans plans_pkey; Type: CONSTRAINT; Schema: public; Owner: tenders
--

ALTER TABLE ONLY public.plans
    ADD CONSTRAINT plans_pkey PRIMARY KEY (id);


--
-- Name: refresh_tokens refresh_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: tenders
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_pkey PRIMARY KEY (id);


--
-- Name: refresh_tokens refresh_tokens_token_hash_key; Type: CONSTRAINT; Schema: public; Owner: tenders
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_token_hash_key UNIQUE (token_hash);


--
-- Name: user_applications user_applications_pkey; Type: CONSTRAINT; Schema: public; Owner: tenders
--

ALTER TABLE ONLY public.user_applications
    ADD CONSTRAINT user_applications_pkey PRIMARY KEY (id);


--
-- Name: user_applications user_applications_user_id_tender_id_key; Type: CONSTRAINT; Schema: public; Owner: tenders
--

ALTER TABLE ONLY public.user_applications
    ADD CONSTRAINT user_applications_user_id_tender_id_key UNIQUE (user_id, tender_id);


--
-- Name: user_institutions user_institutions_pkey; Type: CONSTRAINT; Schema: public; Owner: tenders
--

ALTER TABLE ONLY public.user_institutions
    ADD CONSTRAINT user_institutions_pkey PRIMARY KEY (user_id, institution_slug);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: tenders
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: tenders
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: refresh_tokens refresh_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tenders
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: user_applications user_applications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tenders
--

ALTER TABLE ONLY public.user_applications
    ADD CONSTRAINT user_applications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: user_institutions user_institutions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tenders
--

ALTER TABLE ONLY public.user_institutions
    ADD CONSTRAINT user_institutions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict bgONmQHEKpYVk6l3dmh5SAy49qNszaahWO9IGgKYuGf6SwpVLaLDTqKawFkmljq

