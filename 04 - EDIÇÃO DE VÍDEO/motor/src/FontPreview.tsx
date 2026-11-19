import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {PAIRS} from './fonts';

export const FontPreview: React.FC<{pair: number}> = ({pair}) => {
	const p = PAIRS[pair];
	const shadow = '0 4px 30px rgba(0,0,0,0.55)';
	return (
		<AbsoluteFill style={{backgroundColor: '#000'}}>
			<Img src={staticFile('broll/_preview/top.jpg')} style={{position: 'absolute', top: 0, width: 1080, height: 960, objectFit: 'cover'}} />
			<Img src={staticFile('broll/_preview/bottom.jpg')} style={{position: 'absolute', top: 960, width: 1080, height: 960, objectFit: 'cover'}} />
			{/* legibility band at the seam */}
			<AbsoluteFill style={{background: 'linear-gradient(180deg, transparent 38%, rgba(0,0,0,0.38) 50%, transparent 62%)'}} />
			<AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', textAlign: 'center', color: '#fff'}}>
				<div style={{fontFamily: p.base.family, fontWeight: p.base.weight, letterSpacing: p.base.tracking, fontSize: 46, opacity: 0.88, textShadow: shadow}}>
					Marcas de
				</div>
				<div
					style={{
						fontFamily: p.keyword.family,
						fontWeight: p.keyword.weight,
						fontStyle: p.keyword.style,
						letterSpacing: p.keyword.tracking,
						fontSize: p.keyword.size,
						lineHeight: 0.95,
						margin: '6px 0 10px',
						textShadow: shadow,
					}}
				>
					luxo
				</div>
				<div style={{fontFamily: p.base.family, fontWeight: p.base.weight, letterSpacing: p.base.tracking, fontSize: 46, opacity: 0.88, textShadow: shadow}}>
					vendem significado
				</div>
			</AbsoluteFill>
			<div
				style={{
					position: 'absolute',
					top: 48,
					left: 48,
					padding: '14px 26px',
					borderRadius: 999,
					background: 'rgba(0,0,0,0.65)',
					color: '#fff',
					fontFamily: p.base.family,
					fontWeight: 500,
					fontSize: 34,
				}}
			>
				{p.id} · {p.name}
			</div>
		</AbsoluteFill>
	);
};
