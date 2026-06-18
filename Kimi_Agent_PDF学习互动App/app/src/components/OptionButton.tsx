import { motion } from 'framer-motion';
import { CheckCircle, XCircle } from 'lucide-react';

interface OptionButtonProps {
  label: string;
  value: string;
  selected: boolean;
  state: 'idle' | 'correct' | 'wrong' | 'other';
  onClick: () => void;
  disabled: boolean;
}

export default function OptionButton({ label, value, selected, state, onClick, disabled }: OptionButtonProps) {
  const getStyles = () => {
    switch (state) {
      case 'correct':
        return 'border-[#2ECC71] bg-[#E8F8E8] shadow-md';
      case 'wrong':
        return 'border-[#E74C3C] bg-[#FDE8E8] shadow-md';
      case 'other':
        return 'border-gray-200 bg-white opacity-60';
      default:
        if (selected) return 'border-[#FF6B35] bg-[#FFF5F0] shadow-md';
        return 'border-gray-200 bg-white hover:border-[#FF6B35] hover:bg-[#FFF5F0]';
    }
  };

  return (
    <motion.button
      whileHover={!disabled ? { scale: 1.02 } : {}}
      whileTap={!disabled ? { scale: 0.98 } : {}}
      onClick={onClick}
      disabled={disabled}
      className={`relative w-full p-4 rounded-2xl border-2 text-left transition-all duration-200 ${getStyles()} ${disabled && state === 'idle' && !selected ? 'cursor-not-allowed opacity-70' : ''}`}
    >
      <div className="flex items-center gap-3">
        <span
          className={`flex-shrink-0 w-10 h-10 rounded-xl flex items-center justify-center text-lg font-bold ${
            state === 'correct'
              ? 'bg-[#2ECC71] text-white'
              : state === 'wrong'
              ? 'bg-[#E74C3C] text-white'
              : selected
              ? 'bg-[#FF6B35] text-white'
              : 'bg-gray-100 text-[#2C3E50]'
          }`}
          style={{ fontFamily: 'Nunito, sans-serif' }}
        >
          {label}
        </span>
        <span
          className="text-base sm:text-lg font-semibold text-[#2C3E50] leading-snug"
          style={{ fontFamily: 'Nunito, sans-serif' }}
        >
          {value}
        </span>

        {state === 'correct' && (
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', stiffness: 500, damping: 15 }}
            className="ml-auto"
          >
            <CheckCircle className="w-6 h-6 text-[#2ECC71]" />
          </motion.div>
        )}
        {state === 'wrong' && (
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', stiffness: 500, damping: 15 }}
            className="ml-auto"
          >
            <XCircle className="w-6 h-6 text-[#E74C3C]" />
          </motion.div>
        )}
      </div>
    </motion.button>
  );
}
