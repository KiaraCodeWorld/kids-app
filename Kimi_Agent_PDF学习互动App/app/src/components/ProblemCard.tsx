import { motion } from 'framer-motion';
import { Star, Send } from 'lucide-react';
import type { Problem } from '../types/problem';
import OptionButton from './OptionButton';

interface ProblemCardProps {
  problem: Problem;
  selectedOption: string | null;
  answerSubmitted: boolean;
  isCorrect: boolean;
  onSelectOption: (label: string) => void;
  onSubmit: () => void;
}

export default function ProblemCard({
  problem,
  selectedOption,
  answerSubmitted,
  isCorrect,
  onSelectOption,
  onSubmit,
}: ProblemCardProps) {
  const getOptionState = (label: string): 'idle' | 'correct' | 'wrong' | 'other' => {
    if (!answerSubmitted) return 'idle';
    if (label === problem.correctAnswer) return 'correct';
    if (label === selectedOption && !isCorrect) return 'wrong';
    return 'other';
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -50 }}
      transition={{ duration: 0.4, ease: 'easeOut' }}
      className="bg-white rounded-3xl p-5 sm:p-8 shadow-lg"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-5">
        <span
          className="bg-[#FF6B35] text-white text-sm font-bold px-4 py-1.5 rounded-full"
          style={{ fontFamily: 'Nunito, sans-serif' }}
        >
          Question {problem.id}
        </span>
        <span
          className="bg-[#FFE66D] text-[#2C3E50] text-sm font-semibold px-3 py-1.5 rounded-full flex items-center gap-1"
          style={{ fontFamily: 'Nunito, sans-serif' }}
        >
          <Star className="w-4 h-4 fill-[#2C3E50]" />
          {problem.points} point{problem.points > 1 ? 's' : ''}
        </span>
      </div>

      {/* Problem Image (if available) */}
      {problem.image && (
        <div className="mb-4 rounded-xl overflow-hidden border-2 border-gray-100">
          <img
            src={problem.image}
            alt={`Diagram for question ${problem.id}`}
            className="w-full h-auto max-h-64 object-contain bg-white"
            loading="lazy"
          />
        </div>
      )}

      {/* Problem Text */}
      <div className="mb-6">
        <p
          className="text-lg sm:text-xl font-semibold text-[#2C3E50] leading-relaxed whitespace-pre-line"
          style={{ fontFamily: 'Nunito, sans-serif' }}
        >
          {problem.question}
        </p>
      </div>

      {/* Options Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-6">
        {problem.options.map((option) => (
          <OptionButton
            key={option.label}
            label={option.label}
            value={option.value}
            selected={selectedOption === option.label}
            state={getOptionState(option.label)}
            onClick={() => onSelectOption(option.label)}
            disabled={answerSubmitted}
          />
        ))}
      </div>

      {/* Submit Button */}
      {!answerSubmitted && (
        <motion.button
          whileHover={selectedOption ? { scale: 1.02 } : {}}
          whileTap={selectedOption ? { scale: 0.98 } : {}}
          onClick={onSubmit}
          disabled={!selectedOption}
          className={`w-full py-3.5 rounded-full text-lg font-bold flex items-center justify-center gap-2 transition-all duration-200 ${
            selectedOption
              ? 'bg-[#FF6B35] text-white shadow-md hover:shadow-lg cursor-pointer'
              : 'bg-gray-200 text-gray-400 cursor-not-allowed'
          }`}
          style={{ fontFamily: 'Nunito, sans-serif' }}
        >
          <Send className="w-5 h-5" />
          Check My Answer!
        </motion.button>
      )}
    </motion.div>
  );
}
