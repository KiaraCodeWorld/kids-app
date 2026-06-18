import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { Trophy, Star, RotateCcw, Award } from 'lucide-react';
import confetti from 'canvas-confetti';

interface CelebrationScreenProps {
  score: number;
  totalQuestions: number;
  onReset: () => void;
}

export default function CelebrationScreen({ score, totalQuestions, onReset }: CelebrationScreenProps) {
  useEffect(() => {
    // Fire confetti
    const duration = 5 * 1000;
    const animationEnd = Date.now() + duration;
    const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 100 };

    const randomInRange = (min: number, max: number) => Math.random() * (max - min) + min;

    const interval = setInterval(() => {
      const timeLeft = animationEnd - Date.now();
      if (timeLeft <= 0) {
        clearInterval(interval);
        return;
      }

      const particleCount = 50 * (timeLeft / duration);

      confetti({
        ...defaults,
        particleCount,
        origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 },
        colors: ['#FF6B35', '#4ECDC4', '#FFE66D', '#2ECC71', '#E74C3C'],
      });
      confetti({
        ...defaults,
        particleCount,
        origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 },
        colors: ['#FF6B35', '#4ECDC4', '#FFE66D', '#2ECC71', '#E74C3C'],
      });
    }, 250);

    return () => clearInterval(interval);
  }, []);

  const percentage = Math.round((score / totalQuestions) * 100);

  const getMessage = () => {
    if (percentage === 100) return "Perfect Score! You're a Math Genius! 🌟";
    if (percentage >= 80) return "Outstanding work! You're a Math Champion! 🏆";
    if (percentage >= 60) return "Great job! Keep practicing and you'll be a master! 💪";
    return "Good effort! Every problem you try makes you stronger! 🌱";
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-20">
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.6, ease: 'easeOut' }}
        className="max-w-md w-full text-center"
      >
        {/* Trophy */}
        <motion.div
          initial={{ y: -20 }}
          animate={{ y: [0, -10, 0] }}
          transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
          className="mb-6"
        >
          <div className="w-28 h-28 bg-gradient-to-br from-[#FFE66D] to-[#FF6B35] rounded-full flex items-center justify-center mx-auto shadow-xl">
            <Trophy className="w-14 h-14 text-white" />
          </div>
        </motion.div>

        <h1
          className="text-3xl sm:text-4xl font-extrabold text-[#2C3E50] mb-3"
          style={{ fontFamily: 'Nunito, sans-serif' }}
        >
          🎉 Math Adventure Complete! 🎉
        </h1>

        <p
          className="text-lg text-[#7F8C8D] mb-8"
          style={{ fontFamily: 'Nunito, sans-serif' }}
        >
          {getMessage()}
        </p>

        {/* Score Card */}
        <div className="bg-white rounded-3xl p-6 shadow-lg mb-8">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Award className="w-6 h-6 text-[#FF6B35]" />
            <span
              className="text-xl font-bold text-[#2C3E50]"
              style={{ fontFamily: 'Nunito, sans-serif' }}
            >
              Your Score
            </span>
          </div>

          <div className="flex items-center justify-center gap-3 mb-4">
            {Array.from({ length: 5 }, (_, i) => {
              const threshold = (i + 1) * 20;
              const filled = percentage >= threshold;
              return (
                <Star
                  key={i}
                  className={`w-8 h-8 sm:w-10 sm:h-10 transition-all duration-500 ${
                    filled ? 'text-[#FFE66D] fill-[#FFE66D] scale-110' : 'text-gray-200'
                  }`}
                  style={{ transitionDelay: `${i * 200}ms` }}
                />
              );
            })}
          </div>

          <div className="text-4xl sm:text-5xl font-extrabold text-[#FF6B35] mb-2" style={{ fontFamily: 'Nunito, sans-serif' }}>
            {score} <span className="text-2xl text-[#7F8C8D]">/ {totalQuestions}</span>
          </div>

          <div
            className="text-lg font-semibold text-[#4ECDC4]"
            style={{ fontFamily: 'Nunito, sans-serif' }}
          >
            {percentage}% Correct
          </div>
        </div>

        {/* Reset Button */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={onReset}
          className="bg-[#FF6B35] text-white text-lg font-bold px-10 py-4 rounded-full shadow-lg hover:shadow-xl transition-all duration-200 flex items-center gap-2 mx-auto"
          style={{ fontFamily: 'Nunito, sans-serif' }}
        >
          <RotateCcw className="w-5 h-5" />
          Start Over
        </motion.button>
      </motion.div>
    </div>
  );
}
