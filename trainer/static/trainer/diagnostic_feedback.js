/**
 * Diagnostic feedback for common math mistakes.
 * Returns a short, encouraging hint based on the question, user answer, and correct answer.
 */
function diagnoseMathMistake(question, userAnswer, correctAnswer) {
    const ua = parseFloat(userAnswer);
    const ca = parseFloat(correctAnswer);
    const q = (question || '').toLowerCase();

    if (isNaN(ua) || isNaN(ca)) {
        return "Check the question again — make sure you answered what was asked.";
    }

    const diff = Math.abs(ua - ca);

    // Off-by-one
    if (diff === 1) {
        return "You were super close! Double-check your counting by one.";
    }

    // Off-by-ten: likely place-value slip
    if (diff === 10 || (diff > 0 && diff % 10 === 0 && diff < 100)) {
        return "Check your tens and ones — it looks like a place-value slip.";
    }

    // Sign error: added instead of subtracted or vice versa
    if ((q.includes('add') || q.includes('plus') || q.includes('+')) && ua < ca) {
        return "Make sure you added both numbers together.";
    }
    if ((q.includes('subtract') || q.includes('minus') || q.includes('take away') || q.includes('−') || q.includes('-')) && ua > ca) {
        return "Make sure you subtracted the smaller number from the bigger one.";
    }

    // Multiplication/division
    if ((q.includes('multiply') || q.includes('times') || q.includes('×') || q.includes('each')) && diff > 1) {
        return "Try thinking in groups — how many groups of one number fit into the other?";
    }
    if ((q.includes('divide') || q.includes('split') || q.includes('share') || q.includes('÷')) && diff > 1) {
        return "Sharing equally is the key — how many would each group get?";
    }

    // Fractions
    if (q.includes('fraction') || q.includes('half') || q.includes('quarter') || q.includes('third')) {
        return "Remember: the bottom number tells how many equal parts, and the top tells how many you have.";
    }

    // Money / time
    if (q.includes('dollar') || q.includes('cent') || q.includes('$') || q.includes('money')) {
        return "Count the dollars and cents separately, then add them together.";
    }
    if (q.includes('hour') || q.includes('minute') || q.includes('clock') || q.includes('time')) {
        return "Take it step by step — hours first, then minutes.";
    }

    // Default encouraging hint
    return "Try breaking the problem into smaller steps. You've got this!";
}
