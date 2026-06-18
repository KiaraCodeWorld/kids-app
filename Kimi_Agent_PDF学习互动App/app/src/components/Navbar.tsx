import { Star, BookOpen } from 'lucide-react';
import { motion } from 'framer-motion';

interface NavbarProps {
  currentQuestion: number;
  totalQuestions: number;
  score: number;
  visible: boolean;
}

export default function Navbar({ currentQuestion, totalQuestions, score, visible }: NavbarProps) {
  if (!visible) return null;

  const progress = ((currentQuestion) / totalQuestions) * 100;

  return (
    <motion.nav
      initial={{ y: -80 }}
      animate={{ y: 0 }}
      className="fixed top-0 left-0 right-0 h-16 bg-white shadow-md z-50 flex items-center px-4 md:px-8"
    >
      <div className="flex items-center gap-2 flex-shrink-0">
        <BookOpen className="w-7 h-7 text-[#FF6B35]" />
        <span className="text-xl font-extrabold text-[#FF6B35] hidden sm:inline" style={{ fontFamily: 'Nunito, sans-serif' }}>
          Math Quest
        </span>
      </div>

      <div className="flex-1 mx-4 md:mx-12 max-w-xl">
        <div className="flex items-center gap-3">
          <span className="text-sm font-semibold text-[#2C3E50] whitespace-nowrap" style={{ fontFamily: 'Nunito, sans-serif' }}>
            Q{Math.min(currentQuestion + 1, totalQuestions)} of {totalQuestions}
          </span>
          <div className="flex-1 h-3 bg-gray-200 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-[#FF6B35] to-[#FFE66D] rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.5, ease: 'easeOut' }}
            />
          </div>
        </div>
      </div>

      <div className="flex items-center gap-2 flex-shrink-0">
        <Star className="w-6 h-6 text-[#FFE66D] fill-[#FFE66D]" />
        <span className="text-lg font-bold text-[#2C3E50]" style={{ fontFamily: 'Nunito, sans-serif' }}>
          {score}
        </span>
        <span className="text-sm text-gray-400 hidden sm:inline" style={{ fontFamily: 'Nunito, sans-serif' }}>
          / {totalQuestions}
        </span>
      </div>
    </motion.nav>
  );
}
