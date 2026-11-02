import React from "react";
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from "remotion";
import timeline from "./timeline.json";

const FPS = timeline.fps;
const DISPLAY = "'Inter Display', 'Inter', sans-serif";
const MONO = "'JetBrains Mono', monospace";
const ease = Easing.bezier(0.16, 1, 0.3, 1);
const s = (sec: number) => Math.round(sec * FPS);
const shadow = "0 1px 2px rgba(0,0,0,0.35), 0 0 24px rgba(0,0,0,0.35)";

const fade = (f: number, a: number, b: number, c: number, d: number) =>
	interpolate(f, [a, b, c, d], [0, 1, 1, 0], {
		extrapolateLeft: "clamp",
		extrapolateRight: "clamp",
		easing: ease,
	});

/* ── Opening title ──────────────────────────────────────────── */
const Title: React.FC<{f: number}> = ({f}) => {
	const inA = s(0.55);
	const outB = s(2.95);
	const p = interpolate(f, [inA, inA + s(1.3)], [0, 1], {
		extrapolateLeft: "clamp",
		extrapolateRight: "clamp",
		easing: ease,
	});
	const out = interpolate(f, [outB - s(0.3), outB], [0, 1], {
		extrapolateLeft: "clamp",
		extrapolateRight: "clamp",
		easing: Easing.in(Easing.cubic),
	});
	const sub = interpolate(f, [s(1.05), s(1.75)], [0, 1], {
		extrapolateLeft: "clamp",
		extrapolateRight: "clamp",
		easing: ease,
	});
	if (f < inA || f > outB) return null;
	return (
		<AbsoluteFill style={{alignItems: "center", justifyContent: "center"}}>
			<AbsoluteFill
				style={{
					background:
						"radial-gradient(ellipse 55% 45% at 50% 50%, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.18) 70%, rgba(0,0,0,0.12) 100%)",
					opacity: p * (1 - out),
				}}
			/>
			<div
				style={{
					fontFamily: DISPLAY,
					fontWeight: 200,
					fontSize: 200,
					color: "white",
					letterSpacing: `${0.34 - 0.26 * p + 0.06 * out}em`,
					marginRight: `-${0.34 - 0.26 * p + 0.06 * out}em`,
					opacity: p * (1 - out),
					filter: `blur(${(1 - p) * 14 + out * 8}px)`,
					textShadow: shadow,
					lineHeight: 1,
					fontVariantNumeric: "tabular-nums",
				}}
			>
				29.10
			</div>
			<div
				style={{
					width: 140 * sub,
					height: 1,
					background: "rgba(255,255,255,0.8)",
					margin: "34px 0 26px",
					opacity: 1 - out,
				}}
			/>
			<div
				style={{
					fontFamily: MONO,
					fontWeight: 600,
					fontSize: 21,
					letterSpacing: "0.55em",
					marginRight: "-0.55em",
					color: "white",
					opacity: sub * (1 - out) * 0.92,
					transform: `translateY(${(1 - sub) * 10}px)`,
					textShadow: shadow,
				}}
			>
				UM DIA DE MEDICINA
			</div>
		</AbsoluteFill>
	);
};

/* ── Clock HUD: digits roll on every cut ────────────────────── */
const ROLL = 7;
const Digit: React.FC<{prev: string; next: string; local: number}> = ({prev, next, local}) => {
	const changing = prev !== next;
	const p = changing
		? interpolate(local, [0, ROLL], [0, 1], {
				extrapolateLeft: "clamp",
				extrapolateRight: "clamp",
				easing: ease,
			})
		: 1;
	const cell: React.CSSProperties = {position: "absolute", left: 0, top: 0, width: "100%"};
	return (
		<span
			style={{
				position: "relative",
				display: "inline-block",
				width: "0.62em",
				height: "1.2em",
				overflow: "hidden",
				textAlign: "center",
			}}
		>
			{changing && (
				<span style={{...cell, transform: `translateY(${-p * 100}%)`, opacity: 1 - p}}>{prev}</span>
			)}
			<span style={{...cell, transform: `translateY(${(1 - p) * 100}%)`, opacity: p}}>{next}</span>
		</span>
	);
};

const Clock: React.FC<{f: number}> = ({f}) => {
	const stamps = timeline.stamps as [number, string][];
	const start = s(stamps[0][0]);
	const end = s(timeline.stampsEnd);
	if (f < start || f >= end) return null;
	let idx = 0;
	stamps.forEach(([t], i) => {
		if (f >= s(t)) idx = i;
	});
	const cur = stamps[idx][1];
	const prev = idx > 0 ? stamps[idx - 1][1] : "  :  ";
	const local = f - s(stamps[idx][0]);
	const vis = fade(f, start, start + s(0.5), end - 4, end);
	const line = interpolate(f, [start, start + s(0.6)], [0, 1], {
		extrapolateLeft: "clamp",
		extrapolateRight: "clamp",
		easing: ease,
	});
	return (
		<div
			style={{
				position: "absolute",
				left: 76,
				bottom: 62,
				display: "flex",
				alignItems: "center",
				gap: 16,
				opacity: vis,
				color: "white",
				textShadow: shadow,
			}}
		>
			<div style={{width: 1, height: 38 * line, background: "rgba(255,255,255,0.85)"}} />
			<div style={{display: "flex", flexDirection: "column", gap: 4}}>
				<div
					style={{
						fontFamily: MONO,
						fontSize: 13,
						fontWeight: 600,
						letterSpacing: "0.42em",
						opacity: 0.8,
					}}
				>
					29.10
				</div>
				<div
					style={{
						fontFamily: MONO,
						fontWeight: 500,
						fontSize: 32,
						letterSpacing: "0.04em",
						display: "flex",
						lineHeight: 1.2,
					}}
				>
					{cur.split("").map((c, i) => (
						<Digit key={i} prev={prev[i] ?? " "} next={c} local={local} />
					))}
				</div>
			</div>
		</div>
	);
};

/* ── End card (left of the group photo) ─────────────────────── */
const EndCard: React.FC<{f: number}> = ({f}) => {
	const a = s(25.45);
	const end = s(30);
	if (f < a) return null;
	const p = interpolate(f, [a, a + s(1.4)], [0, 1], {
		extrapolateLeft: "clamp",
		extrapolateRight: "clamp",
		easing: ease,
	});
	const p2 = interpolate(f, [a + s(0.5), a + s(1.6)], [0, 1], {
		extrapolateLeft: "clamp",
		extrapolateRight: "clamp",
		easing: ease,
	});
	const out = interpolate(f, [s(28.6), end], [0, 1], {
		extrapolateLeft: "clamp",
		extrapolateRight: "clamp",
	});
	return (
		<div
			style={{
				position: "absolute",
				left: 0,
				top: 0,
				width: 960,
				height: 1080,
				display: "flex",
				flexDirection: "column",
				alignItems: "center",
				justifyContent: "center",
				color: "white",
				textShadow: shadow,
				opacity: 1 - out,
			}}
		>
			<div
				style={{
					fontFamily: DISPLAY,
					fontWeight: 200,
					fontSize: 150,
					lineHeight: 1,
					letterSpacing: `${0.24 - 0.16 * p}em`,
					marginRight: `-${0.24 - 0.16 * p}em`,
					opacity: p,
					filter: `blur(${(1 - p) * 10}px)`,
				}}
			>
				29.10
			</div>
			<div style={{width: 110 * p2, height: 1, background: "rgba(255,255,255,0.8)", margin: "30px 0 24px"}} />
			<div
				style={{
					fontFamily: MONO,
					fontSize: 24,
					letterSpacing: "0.14em",
					opacity: p2,
					transform: `translateY(${(1 - p2) * 10}px)`,
				}}
			>
				12:21 → 17:28
			</div>
			<div
				style={{
					fontFamily: MONO,
					fontSize: 13,
					letterSpacing: "0.6em",
					marginRight: "-0.6em",
					marginTop: 18,
					opacity: p2 * 0.75,
				}}
			>
				UM DIA DE MEDICINA
			</div>
		</div>
	);
};

export const Type: React.FC = () => {
	const f = useCurrentFrame();
	return (
		<AbsoluteFill style={{backgroundColor: "transparent"}}>
			<Title f={f} />
			<Clock f={f} />
			<EndCard f={f} />
		</AbsoluteFill>
	);
};
