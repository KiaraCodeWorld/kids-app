import { useMemo } from 'react';
import { motion } from 'framer-motion';

const SYMBOLS = ['+', '-', '×', '÷', '=', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'];

interface FloatingSymbol {
  id: number;
  symbol: string;
  left: number;
  size: number;
  duration: number;
  delay: number;
  drift: number;
}

export default function FloatingSymbols() {
  const symbols = useMemo<FloatingSymbol[]>(() => {
    return Array.from({ length: 18 }, (_, i) => ({
      id: i,
      symbol: SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)],
      left: Math.random() * 100,
      size: 20 + Math.random() * 30,
      duration: 15 + Math.random() * 12,
      delay: Math.random() * 15,
      drift: (Math.random() - 0.5) * 200,
    }));
  }, []);

  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
      {symbols.map((s) => (
        <motion.div
          key={s.id}
          className="absolute text-[#FF6B35] select-none font-bold"
          style={{
            left: `${s.left}%`,
            fontSize: `${s.size}px`,
            opacity: 0.12,
          }}
          initial={{ y: '110vh', rotate: 0 }}
          animate={{
            y: '-10vh',
            rotate: 360,
            x: s.drift,
          }}
          transition={{
            duration: s.duration,
            delay: s.delay,
            repeat: Infinity,
            ease: 'linear',
          }}
        >
          {s.symbol}
        </motion.div>
      ))}
    </div>
  );
}
