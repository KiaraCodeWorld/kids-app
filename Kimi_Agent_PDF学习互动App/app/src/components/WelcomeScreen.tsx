import { motion } from 'framer-motion';
import { Rocket, Star, Brain } from 'lucide-react';

interface WelcomeScreenProps {
  onStart: () => void;
  totalQuestions: number;
}

export default function WelcomeScreen({ onStart, totalQuestions }: WelcomeScreenProps) {
  return (
    <div className="min-h-screen flex items-center justify-center px-4 sm:px-6 relative">
      <div className="max-w-lg w-full text-center relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
        >
          <div className="flex justify-center mb-4">
            <div className="w-20 h-20 bg-[#FF6B35] rounded-3xl flex items-center justify-center shadow-lg">
              <Brain className="w-10 h-10 text-white" />
            </div>
          </div>

          <p
            className="text-sm font-semibold uppercase tracking-[2px] text-[#4ECDC4] mb-3"
            style={{ fontFamily: 'Nunito, sans-serif' }}
          >
            Grade 3-4 Math Olympiad
          </p>

          <h1
            className="text-4xl sm:text-5xl font-extrabold text-[#2C3E50] mb-4 leading-tight"
            style={{ fontFamily: 'Nunito, sans-serif' }}
          >
            Ready for a Math Adventure?{' '}
            <Rocket className="inline-block w-10 h-10 text-[#FF6B35] -mt-1" />
          </h1>
        </motion.div>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: 'easeOut', delay: 0.2 }}
          className="text-lg text-[#7F8C8D] mb-8 max-w-md mx-auto leading-relaxed"
          style={{ fontFamily: 'Nunito, sans-serif' }}
        >
          Solve fun math problems one by one. Your Math Buddy will help you learn!
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: 'easeOut', delay: 0.4 }}
          className="flex flex-col items-center gap-4"
        >
          <button
            onClick={onStart}
            className="bg-[#FF6B35] text-white text-xl font-bold px-12 py-4 rounded-full shadow-lg hover:shadow-xl hover:scale-105 active:scale-95 transition-all duration-200"
            style={{ fontFamily: 'Nunito, sans-serif' }}
          >
            Start Solving!
          </button>

          <p
            className="text-sm text-[#7F8C8D] flex items-center gap-1"
            style={{ fontFamily: 'Nunito, sans-serif' }}
          >
            <Star className="w-4 h-4 text-[#FFE66D] fill-[#FFE66D]" />
            {totalQuestions} problems • Get a star for each correct answer
          </p>
        </motion.div>
      </div>
    </div>
  );
}
