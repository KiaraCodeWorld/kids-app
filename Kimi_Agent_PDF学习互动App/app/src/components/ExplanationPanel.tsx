import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronRight, BookOpen, Sparkles } from 'lucide-react';

interface ExplanationPanelProps {
  steps: string[];
  keyConcept: string;
  visible: boolean;
}

export default function ExplanationPanel({ steps, keyConcept, visible }: ExplanationPanelProps) {
  const [revealedSteps, setRevealedSteps] = useState(0);
  const [showAll, setShowAll] = useState(false);

  if (!visible) return null;

  const handleNextStep = () => {
    if (revealedSteps < steps.length) {
      setRevealedSteps(revealedSteps + 1);
    }
  };

  const handleShowAll = () => {
    setRevealedSteps(steps.length);
    setShowAll(true);
  };

  const currentSteps = showAll ? steps : steps.slice(0, revealedSteps);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.3 }}
      className="bg-white rounded-2xl p-5 sm:p-6 border-l-4 border-[#4ECDC4] shadow-md"
    >
      <div className="flex items-center gap-2 mb-4">
        <BookOpen className="w-5 h-5 text-[#4ECDC4]" />
        <h3
          className="text-lg sm:text-xl font-bold text-[#2C3E50]"
          style={{ fontFamily: 'Nunito, sans-serif' }}
        >
          Here's How to Solve It!
        </h3>
      </div>

      <div className="space-y-3">
        <AnimatePresence>
          {currentSteps.map((step, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3 }}
              className="flex gap-3 items-start"
            >
              <span
                className="flex-shrink-0 w-7 h-7 rounded-full bg-[#4ECDC4] text-white flex items-center justify-center text-sm font-bold mt-0.5"
                style={{ fontFamily: 'Nunito, sans-serif' }}
              >
                {index + 1}
              </span>
              <p
                className="text-[#2C3E50] text-sm sm:text-base leading-relaxed whitespace-pre-line"
                style={{ fontFamily: 'Nunito, sans-serif' }}
              >
                {step}
              </p>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {/* Navigation Buttons */}
      {revealedSteps < steps.length && (
        <div className="flex gap-3 mt-4">
          <button
            onClick={handleNextStep}
            className="flex items-center gap-1 bg-[#4ECDC4] text-white px-4 py-2 rounded-full text-sm font-semibold hover:bg-[#3DBDB5] transition-colors"
            style={{ fontFamily: 'Nunito, sans-serif' }}
          >
            <ChevronRight className="w-4 h-4" />
            Show Next Step
          </button>
          <button
            onClick={handleShowAll}
            className="text-[#7F8C8D] text-sm font-semibold hover:text-[#4ECDC4] transition-colors underline"
            style={{ fontFamily: 'Nunito, sans-serif' }}
          >
            Show All Steps
          </button>
        </div>
      )}

      {/* Key Concept Box */}
      {revealedSteps >= steps.length && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="mt-4 bg-[#FFF9E6] rounded-xl p-4 flex gap-3 items-start"
        >
          <Sparkles className="w-5 h-5 text-[#FFE66D] flex-shrink-0 mt-0.5" />
          <div>
            <p
              className="text-sm font-bold text-[#2C3E50] mb-1"
              style={{ fontFamily: 'Nunito, sans-serif' }}
            >
              💡 Remember:
            </p>
            <p
              className="text-sm text-[#2C3E50] leading-relaxed"
              style={{ fontFamily: 'Nunito, sans-serif' }}
            >
              {keyConcept}
            </p>
          </div>
        </motion.div>
      )}
    </motion.div>
  );
}
