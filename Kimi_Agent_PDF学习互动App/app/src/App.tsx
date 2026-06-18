import { useState, useCallback, useEffect } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { ArrowLeft, ArrowRight, Star } from 'lucide-react';
import { problems } from './data/problems';
import FloatingSymbols from './components/FloatingSymbols';
import Navbar from './components/Navbar';
import WelcomeScreen from './components/WelcomeScreen';
import ProblemCard from './components/ProblemCard';
import MathBuddy from './components/MathBuddy';
import ExplanationPanel from './components/ExplanationPanel';
import CelebrationScreen from './components/CelebrationScreen';
import Footer from './components/Footer';

type Screen = 'welcome' | 'problem' | 'celebration';
type BuddyState = 'idle' | 'hint' | 'correct' | 'wrong';

function App() {
  const [screen, setScreen] = useState<Screen>('welcome');
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [answerSubmitted, setAnswerSubmitted] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [buddyState, setBuddyState] = useState<BuddyState>('idle');
  const [score, setScore] = useState(0);
  const [starsEarned, setStarsEarned] = useState<boolean[]>(() => {
    const saved = localStorage.getItem('mathquest_stars');
    return saved ? JSON.parse(saved) : new Array(35).fill(false);
  });

  // Persist stars to localStorage
  useEffect(() => {
    localStorage.setItem('mathquest_stars', JSON.stringify(starsEarned));
  }, [starsEarned]);

  const problem = problems[currentQuestion];

  const handleStart = useCallback(() => {
    setScreen('problem');
  }, []);

  const handleSelectOption = useCallback((label: string) => {
    if (!answerSubmitted) {
      setSelectedOption(label);
    }
  }, [answerSubmitted]);

  const handleSubmit = useCallback(() => {
    if (!selectedOption) return;

    const correct = selectedOption === problem.correctAnswer;
    setIsCorrect(correct);
    setAnswerSubmitted(true);
    setBuddyState(correct ? 'correct' : 'wrong');

    if (correct) {
      const newStars = [...starsEarned];
      if (!newStars[currentQuestion]) {
        newStars[currentQuestion] = true;
        setStarsEarned(newStars);
        setScore(prev => prev + 1);
      }
    }
  }, [selectedOption, problem, currentQuestion, starsEarned]);

  const handleHint = useCallback(() => {
    setBuddyState('hint');
  }, []);

  const handleNext = useCallback(() => {
    if (currentQuestion < problems.length - 1) {
      setCurrentQuestion(prev => prev + 1);
      setSelectedOption(null);
      setAnswerSubmitted(false);
      setIsCorrect(false);
      setBuddyState('idle');
    } else {
      setScreen('celebration');
    }
  }, [currentQuestion]);

  const handlePrev = useCallback(() => {
    if (currentQuestion > 0) {
      setCurrentQuestion(prev => prev - 1);
      setSelectedOption(null);
      setAnswerSubmitted(false);
      setIsCorrect(false);
      setBuddyState('idle');
    }
  }, [currentQuestion]);

  const handleReset = useCallback(() => {
    setCurrentQuestion(0);
    setSelectedOption(null);
    setAnswerSubmitted(false);
    setIsCorrect(false);
    setBuddyState('idle');
    setScore(0);
    setStarsEarned(new Array(35).fill(false));
    setScreen('welcome');
    localStorage.removeItem('mathquest_stars');
  }, []);

  return (
    <div className="min-h-screen bg-[#FFF8F0] relative">
      <FloatingSymbols />

      <Navbar
        currentQuestion={currentQuestion}
        totalQuestions={problems.length}
        score={score}
        visible={screen === 'problem'}
      />

      <main className="relative z-10 pt-0">
        <AnimatePresence mode="wait">
          {screen === 'welcome' && (
            <WelcomeScreen
              key="welcome"
              onStart={handleStart}
              totalQuestions={problems.length}
            />
          )}

          {screen === 'problem' && (
            <motion.div
              key="problem"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="min-h-screen pt-20 pb-8 px-4 sm:px-6 lg:px-8"
            >
              <div className="max-w-6xl mx-auto">
                {/* Star Tracker */}
                <div className="flex flex-wrap justify-center gap-1 mb-6 px-2">
                  {starsEarned.map((earned, i) => (
                    <Star
                      key={i}
                      className={`w-4 h-4 sm:w-5 sm:h-5 transition-all duration-300 ${
                        earned
                          ? 'text-[#FFE66D] fill-[#FFE66D]'
                          : i === currentQuestion
                          ? 'text-[#FF6B35] animate-pulse'
                          : 'text-gray-300'
                      }`}
                    />
                  ))}
                </div>

                {/* Two Column Layout */}
                <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
                  {/* Problem Card */}
                  <div className="lg:col-span-3">
                    <AnimatePresence mode="wait">
                      <ProblemCard
                        key={problem.id}
                        problem={problem}
                        selectedOption={selectedOption}
                        answerSubmitted={answerSubmitted}
                        isCorrect={isCorrect}
                        onSelectOption={handleSelectOption}
                        onSubmit={handleSubmit}
                      />
                    </AnimatePresence>

                    {/* Explanation Panel */}
                    <div className="mt-4">
                      <ExplanationPanel
                        steps={problem.explanation}
                        keyConcept={problem.keyConcept}
                        visible={answerSubmitted}
                      />
                    </div>
                  </div>

                  {/* Math Buddy */}
                  <div className="lg:col-span-2">
                    <div className="lg:sticky lg:top-24">
                      <MathBuddy
                        state={buddyState}
                        hintText={problem.hint}
                        answerSubmitted={answerSubmitted}
                        onHint={handleHint}
                      />

                      {/* Navigation */}
                      {answerSubmitted && (
                        <motion.div
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 0.5 }}
                          className="mt-4 flex items-center justify-between bg-white rounded-2xl p-3 shadow-md"
                        >
                          <button
                            onClick={handlePrev}
                            disabled={currentQuestion === 0}
                            className={`flex items-center gap-1 px-4 py-2 rounded-full text-sm font-semibold transition-all ${
                              currentQuestion === 0
                                ? 'text-gray-300 cursor-not-allowed'
                                : 'text-[#7F8C8D] hover:bg-gray-100'
                            }`}
                            style={{ fontFamily: 'Nunito, sans-serif' }}
                          >
                            <ArrowLeft className="w-4 h-4" />
                            Back
                          </button>

                          <span
                            className="text-sm text-[#7F8C8D] font-medium"
                            style={{ fontFamily: 'Nunito, sans-serif' }}
                          >
                            Q{currentQuestion + 1} of {problems.length}
                          </span>

                          <button
                            onClick={handleNext}
                            className="flex items-center gap-1 bg-[#FF6B35] text-white px-4 py-2 rounded-full text-sm font-semibold hover:bg-[#E55A2B] transition-all shadow-sm"
                            style={{ fontFamily: 'Nunito, sans-serif' }}
                          >
                            {currentQuestion === problems.length - 1 ? 'Finish' : 'Next'}
                            <ArrowRight className="w-4 h-4" />
                          </button>
                        </motion.div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {screen === 'celebration' && (
            <CelebrationScreen
              key="celebration"
              score={score}
              totalQuestions={problems.length}
              onReset={handleReset}
            />
          )}
        </AnimatePresence>
      </main>

      <Footer />
    </div>
  );
}

export default App;
