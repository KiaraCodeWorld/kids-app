import { useState, useEffect, useCallback } from 'react';

export function useTypewriter(text: string, speed: number = 20, enabled: boolean = false) {
  const [displayText, setDisplayText] = useState('');
  const [isComplete, setIsComplete] = useState(false);

  const reset = useCallback(() => {
    setDisplayText('');
    setIsComplete(false);
  }, []);

  useEffect(() => {
    if (!enabled) {
      setDisplayText('');
      setIsComplete(false);
      return;
    }

    reset();
    let index = 0;
    const timer = setInterval(() => {
      if (index < text.length) {
        setDisplayText(text.slice(0, index + 1));
        index++;
      } else {
        setIsComplete(true);
        clearInterval(timer);
      }
    }, speed);

    return () => clearInterval(timer);
  }, [text, speed, enabled, reset]);

  return { displayText, isComplete, reset };
}
