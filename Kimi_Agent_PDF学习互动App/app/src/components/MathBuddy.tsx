import { motion, AnimatePresence } from 'framer-motion';
import { Lightbulb, Sparkles, Sprout, PartyPopper } from 'lucide-react';
import { useTypewriter } from '../hooks/useTypewriter';

interface MathBuddyProps {
  state: 'idle' | 'hint' | 'correct' | 'wrong';
  hintText: string;
  answerSubmitted: boolean;
  onHint: () => void;
}

export default function MathBuddy({ state, hintText, answerSubmitted, onHint }: MathBuddyProps) {
  const getMessage = () => {
    switch (state) {
      case 'correct':
        return "🎉 Amazing! You got it right! Let me explain how to solve it step by step...";
      case 'wrong':
        return "That's okay! Learning from mistakes is how we grow! 🌱 Let me show you how to think about this...";
      case 'hint':
        return hintText;
      default:
        return "Take your time! Read the problem carefully. You've got this! 💪";
    }
  };

  const message = getMessage();
  const { displayText } = useTypewriter(message, 15, state !== 'idle' || answerSubmitted);

  const getIcon = () => {
    switch (state) {
      case 'correct':
        return <PartyPopper className="w-10 h-10 text-[#FF6B35]" />;
      case 'wrong':
        return <Sprout className="w-10 h-10 text-[#4ECDC4]" />;
      case 'hint':
        return <Lightbulb className="w-10 h-10 text-[#FFE66D]" />;
      default:
        return <Sparkles className="w-10 h-10 text-[#4ECDC4]" />;
    }
  };

  return (
    <div className="flex flex-col items-center">
      {/* Character */}
      <motion.div
        animate={{
          y: [0, -6, 0],
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
        className="mb-2"
      >
        <div className="w-20 h-20 bg-gradient-to-br from-[#4ECDC4] to-[#2ECC71] rounded-full flex items-center justify-center shadow-lg">
          {getIcon()}
        </div>
      </motion.div>

      {/* Speech Bubble */}
      <AnimatePresence mode="wait">
        <motion.div
          key={state}
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -30 }}
          transition={{ duration: 0.4 }}
          className="relative bg-[#E8F4FD] rounded-2xl p-5 w-full"
        >
          {/* Triangle pointer */}
          <div className="absolute -top-2 left-1/2 -translate-x-1/2 w-4 h-4 bg-[#E8F4FD] rotate-45" />

          <p
            className="text-[#2C3E50] text-base leading-relaxed relative z-10"
            style={{ fontFamily: 'Nunito, sans-serif' }}
          >
            {answerSubmitted || state === 'hint' ? displayText : message}
          </p>

          {/* Hint Button */}
          {!answerSubmitted && state === 'idle' && (
            <motion.button
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              onClick={onHint}
              className="mt-3 flex items-center gap-1 text-[#4ECDC4] font-semibold text-sm hover:underline transition-all"
              style={{ fontFamily: 'Nunito, sans-serif' }}
            >
              <Lightbulb className="w-4 h-4" />
              Need a hint?
            </motion.button>
          )}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
