import type { Problem } from '../types/problem';

export const problems: Problem[] = [
  {
    id: 1,
    question: "Look at this addition problem:\n\n  3 A 5 4\n  2 6 2 B\n+ C 7 9 3\n-------\n  7 7 7 4\n\nEach letter (A, B, C) stands for a digit. What is A + B + C?",
    options: [
      { label: "A", value: "7" },
      { label: "B", value: "9" },
      { label: "C", value: "10" },
      { label: "D", value: "11" }
    ],
    correctAnswer: "D",
    points: 1,
    hint: "Start from the ones place (rightmost column). What number plus 4 plus 3 gives you 4 or 14?",
    explanation: [
      "Let's start from the rightmost column (ones place): 4 + B + 3 = 4 (or 14 if there's a carry).",
      "4 + B + 3 = 4 doesn't work because B would be negative. So 4 + B + 3 = 14, which means B = 7.",
      "Now the tens place: we carried a 1. So 5 + 2 + 7 + 1 = 15. We write down 5 and carry 1 to the hundreds.",
      "Hundreds place: A + 6 + 9 + 1 (carry) = 17 (or 27). Since the answer has 7 in hundreds place, A + 16 = 17, so A = 1... wait, let me check again: A + 6 + 7 = 17 with carry 1 from before, so A + 6 + 7 + 1 = 17, meaning A = 3.",
      "Thousands place: 3 + 2 + C + 1 (carry) = 7. So C = 1.",
      "Let's verify: A = 3, B = 7, C = 1. So A + B + C = 3 + 7 + 1 = 11!"
    ],
    keyConcept: "When solving multi-digit addition puzzles, always start from the ones place (right side) and work your way left. Watch out for carries!"
  },
  {
    id: 2,
    question: "1899 + MNP = 1217 + 1666\n\nIf MNP is a three-digit number, find MNP.",
    options: [
      { label: "A", value: "943" },
      { label: "B", value: "498" },
      { label: "C", value: "894" },
      { label: "D", value: "984" }
    ],
    correctAnswer: "D",
    points: 2,
    hint: "First figure out what 1217 + 1666 equals. Then use that to find MNP!",
    explanation: [
      "First, let's calculate the right side: 1217 + 1666 = 2883.",
      "So now our equation is: 1899 + MNP = 2883.",
      "To find MNP, we need to do the opposite of addition — subtraction!",
      "MNP = 2883 - 1899 = 984.",
      "Let's check: 1899 + 984 = 2883 ✓ And 1217 + 1666 = 2883 ✓"
    ],
    keyConcept: "When a letter or symbol stands for a number in an equation, first simplify what you can, then use the opposite operation to find the unknown!"
  },
  {
    id: 3,
    question: "Look at this number pattern:\n\n6, ★, 20, ●, 34, 41, ...\n\nHow much more is ● than ★?",
    options: [
      { label: "A", value: "14" },
      { label: "B", value: "15" },
      { label: "C", value: "16" },
      { label: "D", value: "17" }
    ],
    correctAnswer: "A",
    points: 3,
    hint: "Look at the numbers you know: 34 and 41. What's the difference between them? That might be the pattern rule!",
    explanation: [
      "Let's look at the last two numbers we know: 34 and 41.",
      "41 - 34 = 7. So the pattern rule might be 'add 7 each time!'",
      "Let's check: 6 + 7 = 13. So ★ = 13.",
      "13 + 7 = 20. That matches! ✓",
      "20 + 7 = 27. So ● = 27.",
      "27 + 7 = 34. That matches too! ✓",
      "Now we need to find how much more ● is than ★: 27 - 13 = 14."
    ],
    keyConcept: "To find the rule of a number pattern, look at the numbers you already know and find what changes between them!"
  },
  {
    id: 4,
    question: "A greengrocer bought 148 crates of tomatoes to sell. Each crate contained 19 kg of tomatoes. The greengrocer wants to sell these tomatoes in 4 kg packages. How many packages does he need?",
    options: [
      { label: "A", value: "703" },
      { label: "B", value: "73" },
      { label: "C", value: "42" },
      { label: "D", value: "402" }
    ],
    correctAnswer: "A",
    points: 4,
    hint: "First find the total weight of ALL tomatoes. Then figure out how many 4 kg packages you can make.",
    explanation: [
      "Step 1: Find the total weight of all tomatoes.\n148 crates × 19 kg per crate = 2812 kg.",
      "Step 2: Now we need to divide the total weight into 4 kg packages.\n2812 ÷ 4 = 703 packages.",
      "So the greengrocer needs 703 packages!"
    ],
    keyConcept: "When solving word problems, break them into smaller steps. First find the total amount, then divide it into smaller groups!"
  },
  {
    id: 5,
    question: "Read these clues about four children's ages:\n\n• Jack is older than Lily.\n• Lily is younger than Alex, but older than Melissa.\n• Alex is older than Jack.\n\nIf we rank these children from oldest to youngest, who is in 2nd place?",
    options: [
      { label: "A", value: "Jack" },
      { label: "B", value: "Lily" },
      { label: "C", value: "Alex" },
      { label: "D", value: "Melissa" }
    ],
    correctAnswer: "A",
    points: 5,
    hint: "Write down what each clue tells you using > (greater than) symbols. For example: Jack > Lily means Jack is older than Lily.",
    explanation: [
      "Let's use clues one by one:\n• Jack > Lily (Jack is older than Lily)",
      "• Lily < Alex, but Lily > Melissa. So: Alex > Lily > Melissa",
      "• Alex > Jack (Alex is older than Jack)",
      "Putting it all together:\nAlex > Jack > Lily > Melissa",
      "From oldest to youngest: 1st Alex, 2nd Jack, 3rd Lily, 4th Melissa.",
      "So Jack is in 2nd place!"
    ],
    keyConcept: "When solving logic puzzles with 'older than' or 'younger than' clues, write them as inequalities (> or <) and then combine them!"
  },
  {
    id: 6,
    question: "The figure shown is made up of square pieces. What is the minimum number of additional square pieces needed to complete the figure into the smallest possible rectangle?",
    image: "/images/problems/page_2.png",
    options: [
      { label: "A", value: "24" },
      { label: "B", value: "28" },
      { label: "C", value: "30" },
      { label: "D", value: "32" }
    ],
    correctAnswer: "B",
    points: 6,
    hint: "Count how many squares wide and tall the final rectangle should be. Then multiply to find the total squares needed, and subtract the squares you already have.",
    explanation: [
      "The rectangle should be 8 squares wide and 7 squares tall (that's the smallest rectangle that can fit the shape).",
      "Total squares in a complete rectangle = 8 × 7 = 56 squares.",
      "Now count the squares already in the figure. There are 28 squares.",
      "Additional squares needed = 56 - 28 = 28 squares."
    ],
    keyConcept: "To find missing pieces in a shape puzzle, figure out the final size first, then subtract what you already have!"
  },
  {
    id: 7,
    question: "On a farm, the number of chickens is 5 times the number of roosters. If the total number of chickens and roosters is 366, how many chickens are there?",
    options: [
      { label: "A", value: "61" },
      { label: "B", value: "305" },
      { label: "C", value: "73" },
      { label: "D", value: "102" }
    ],
    correctAnswer: "B",
    points: 1,
    hint: "If there is 1 rooster, there are 5 chickens. So together that's 6 birds. How many groups of 6 are in 366?",
    explanation: [
      "Let's say the number of roosters is R. Then chickens = 5 × R.",
      "Total birds: R + 5R = 6R = 366.",
      "So R = 366 ÷ 6 = 61 roosters.",
      "Number of chickens = 5 × 61 = 305 chickens."
    ],
    keyConcept: "When one thing is 'some times' another thing, use a letter (like R) to stand for the smaller amount, then write an equation!"
  },
  {
    id: 8,
    question: "The triple of 106 is added to the quintuple of 95. What is the result of this operation?",
    options: [
      { label: "A", value: "318" },
      { label: "B", value: "475" },
      { label: "C", value: "1608" },
      { label: "D", value: "793" }
    ],
    correctAnswer: "D",
    points: 1,
    hint: "'Triple' means multiply by 3. 'Quintuple' means multiply by 5. Do each multiplication first, then add!",
    explanation: [
      "'Triple of 106' means 3 × 106 = 318.",
      "'Quintuple of 95' means 5 × 95 = 475.",
      "Now add them together: 318 + 475 = 793."
    ],
    keyConcept: "'Triple' means ×3, 'quadruple' means ×4, 'quintuple' means ×5. Learn these fancy words for multiplication!"
  },
  {
    id: 9,
    question: "(3059 × 4) - 879 < ⬜\n\nWhat is the smallest possible value of ⬜?",
    options: [
      { label: "A", value: "11357" },
      { label: "B", value: "11457" },
      { label: "C", value: "11356" },
      { label: "D", value: "11358" }
    ],
    correctAnswer: "D",
    points: 1,
    hint: "First calculate 3059 × 4, then subtract 879. The box needs to be BIGGER than that answer, so what's the very next whole number?",
    explanation: [
      "Step 1: 3059 × 4 = 12236.",
      "Step 2: 12236 - 879 = 11357.",
      "So we need: 11357 < ⬜, meaning ⬜ must be bigger than 11357.",
      "The smallest whole number bigger than 11357 is 11358!"
    ],
    keyConcept: "The < symbol means 'less than.' If we want the smallest number that is BIGGER than something, just add 1!"
  },
  {
    id: 10,
    question: "An athlete needs to run a total of 8746 meters in three days. On the first day, he ran 2104 meters, and on the second day, he ran 3099 meters. How many meters does he need to run on the third day?",
    options: [
      { label: "A", value: "5203" },
      { label: "B", value: "5647" },
      { label: "C", value: "3543" },
      { label: "D", value: "3647" }
    ],
    correctAnswer: "C",
    points: 1,
    hint: "Add up what he already ran on day 1 and day 2. Then subtract that from the total to find what's left for day 3.",
    explanation: [
      "First, find how much he ran in the first two days:\n2104 + 3099 = 5203 meters.",
      "Now subtract from the total:\n8746 - 5203 = 3543 meters.",
      "He needs to run 3543 meters on the third day!"
    ],
    keyConcept: "To find what's REMAINING, add up what you've already used, then subtract from the total!"
  },
  {
    id: 11,
    question: "The product of two numbers is 392. One factor is 8. What is the other factor?",
    options: [
      { label: "A", value: "49" },
      { label: "B", value: "48" },
      { label: "C", value: "39" },
      { label: "D", value: "36" }
    ],
    correctAnswer: "A",
    points: 2,
    hint: "'Product' means multiplication. If 8 × ? = 392, use division (the opposite of multiplication) to find the answer!",
    explanation: [
      "The product of two numbers means we multiply them together.",
      "So: 8 × ? = 392.",
      "To find the missing factor, we divide: 392 ÷ 8 = 49.",
      "Let's check: 8 × 49 = 392 ✓"
    ],
    keyConcept: "Product = multiplication. To find a missing factor, divide the product by the known factor!"
  },
  {
    id: 12,
    question: "18018 ÷ 18\n\nWhich statement about this division is CORRECT?",
    options: [
      { label: "A", value: "The quotient has three digits." },
      { label: "B", value: "The quotient has two zeros." },
      { label: "C", value: "The quotient has one zero." },
      { label: "D", value: "The quotient is the greatest three-digit number." }
    ],
    correctAnswer: "B",
    points: 2,
    hint: "Do the division! 18018 ÷ 18. What number do you get? Then count the zeros and digits.",
    explanation: [
      "Let's calculate: 18018 ÷ 18 = 1001.",
      "1001 has four digits, so A and D are wrong.",
      "1001 has TWO zeros (the two middle zeros), so B is correct!",
      "C says 'one zero' which is wrong — there are two zeros."
    ],
    keyConcept: "Always do the math first! Then check each statement against your answer."
  },
  {
    id: 13,
    question: "3 kg + 2000 mg + 45 g = ? g\n\nWhat is the answer in grams?",
    options: [
      { label: "A", value: "2048" },
      { label: "B", value: "347" },
      { label: "C", value: "3047" },
      { label: "D", value: "5045" }
    ],
    correctAnswer: "C",
    points: 2,
    hint: "Convert everything to grams first! Remember: 1 kg = 1000 g, and 1 g = 1000 mg.",
    explanation: [
      "Convert each measurement to grams:\n• 3 kg = 3 × 1000 = 3000 g",
      "• 2000 mg = 2000 ÷ 1000 = 2 g",
      "• 45 g = 45 g",
      "Now add them: 3000 + 2 + 45 = 3047 g."
    ],
    keyConcept: "When adding measurements, always convert to the SAME unit first! 1 kg = 1000 g, and 1 g = 1000 mg."
  },
  {
    id: 14,
    question: "Oliver's step is 65 cm. Oliver takes 140 steps to go from home to school. What is the distance between his school and his home in meters?",
    options: [
      { label: "A", value: "9100" },
      { label: "B", value: "910" },
      { label: "C", value: "91" },
      { label: "D", value: "90" }
    ],
    correctAnswer: "C",
    points: 2,
    hint: "First find the distance in centimeters (step length × number of steps). Then convert to meters (divide by 100).",
    explanation: [
      "Step 1: Find distance in centimeters.\n65 cm × 140 steps = 9100 cm.",
      "Step 2: Convert to meters.\n9100 cm ÷ 100 = 91 meters.",
      "The distance is 91 meters!"
    ],
    keyConcept: "To convert centimeters to meters, divide by 100. Distance = step length × number of steps!"
  },
  {
    id: 15,
    question: "Emma bought a quarter kilogram of onions, 1 kilogram and 250 grams of tomatoes, 4.5 kilograms of potatoes, 3.5 kilograms of oranges, and half a kilogram of bananas. What is the total weight of all items in kilograms?",
    options: [
      { label: "A", value: "8" },
      { label: "B", value: "9" },
      { label: "C", value: "10" },
      { label: "D", value: "11" }
    ],
    correctAnswer: "C",
    points: 3,
    hint: "Convert everything to kilograms first. Remember: quarter = 0.25, half = 0.5, and 250 g = 0.25 kg.",
    explanation: [
      "Convert all weights to kilograms:\n• Onions: ¼ kg = 0.25 kg",
      "• Tomatoes: 1 kg 250 g = 1.25 kg",
      "• Potatoes: 4.5 kg",
      "• Oranges: 3.5 kg",
      "• Bananas: ½ kg = 0.5 kg",
      "Now add: 0.25 + 1.25 + 4.5 + 3.5 + 0.5 = 10 kg."
    ],
    keyConcept: "When adding mixed measurements, convert everything to the same unit first. Fractions like quarter (¼) = 0.25 and half (½) = 0.5!"
  },
  {
    id: 16,
    question: "How much is 10 quarter-liters less than 5 liters?",
    options: [
      { label: "A", value: "2 liters" },
      { label: "B", value: "2 and a half liters" },
      { label: "C", value: "2 liters and 250 mL" },
      { label: "D", value: "3 liters" }
    ],
    correctAnswer: "B",
    points: 3,
    hint: "A quarter-liter is ¼ liter or 0.25 L. How much is 10 quarter-liters? Then subtract from 5 liters.",
    explanation: [
      "10 quarter-liters = 10 × ¼ = 10/4 = 2.5 liters.",
      "Now subtract from 5 liters: 5 - 2.5 = 2.5 liters.",
      "2.5 liters = 2 and a half liters!"
    ],
    keyConcept: "A quarter-liter (¼ L) = 0.25 liters. Ten quarters equal 2.5, just like ten quarters in money equal $2.50!"
  },
  {
    id: 17,
    question: "A square-shaped field with a side length of 20 meters will be surrounded by 4 rows of wire. How many meters of wire are needed?",
    options: [
      { label: "A", value: "200" },
      { label: "B", value: "240" },
      { label: "C", value: "320" },
      { label: "D", value: "400" }
    ],
    correctAnswer: "C",
    points: 3,
    hint: "First find the perimeter of the field (one row of wire). Then multiply by 4 for the 4 rows.",
    explanation: [
      "Perimeter of square = 4 × side length = 4 × 20 = 80 meters.",
      "This is the length of ONE row of wire.",
      "For 4 rows: 4 × 80 = 320 meters of wire."
    ],
    keyConcept: "Perimeter of a square = 4 × side. If you need multiple rows/layers, multiply the perimeter by the number of rows!"
  },
  {
    id: 18,
    question: "The perimeter of a square is 36 cm. What is the area of the square?",
    options: [
      { label: "A", value: "9" },
      { label: "B", value: "49" },
      { label: "C", value: "64" },
      { label: "D", value: "81" }
    ],
    correctAnswer: "D",
    points: 3,
    hint: "First find the side length from the perimeter. Perimeter = 4 × side. Then area = side × side.",
    explanation: [
      "Perimeter = 4 × side = 36 cm.",
      "So side = 36 ÷ 4 = 9 cm.",
      "Area = side × side = 9 × 9 = 81 cm²."
    ],
    keyConcept: "Perimeter of square = 4 × side. Area of square = side × side. Find the side first, then calculate area!"
  },
  {
    id: 19,
    question: "The perimeter of the shape shown is 68 cm. What is the value of the missing side?\n\nThe shape has sides: 15 cm, 10 cm, 9 cm, 2 cm, 2 cm, 3 cm, 20 cm, and ?",
    options: [
      { label: "A", value: "4" },
      { label: "B", value: "6" },
      { label: "C", value: "7" },
      { label: "D", value: "9" }
    ],
    correctAnswer: "C",
    points: 4,
    hint: "Add up all the sides you know. Then subtract that sum from the total perimeter (68) to find the missing side!",
    explanation: [
      "Add all known sides:\n15 + 10 + 9 + 2 + 2 + 3 + 20 = 61 cm.",
      "The total perimeter is 68 cm.",
      "Missing side = 68 - 61 = 7 cm."
    ],
    keyConcept: "Perimeter is the sum of ALL sides. If one side is missing, add the others and subtract from the total perimeter!"
  },
  {
    id: 20,
    question: "When a grasshopper makes its first jump, it advances 1 meter and 20 centimeters. With each jump, it advances 40 centimeters more than the previous jump. How far will the grasshopper have traveled by the end of its fifth jump?",
    options: [
      { label: "A", value: "1 km" },
      { label: "B", value: "600 cm" },
      { label: "C", value: "10 m" },
      { label: "D", value: "760 cm" }
    ],
    correctAnswer: "C",
    points: 4,
    hint: "Convert the first jump to cm: 1m 20cm = 120 cm. Then add 40 cm for each next jump. Add all 5 jumps together!",
    explanation: [
      "First jump: 1 m 20 cm = 120 cm.",
      "Each jump is 40 cm more than the previous one:\n• Jump 1: 120 cm\n• Jump 2: 160 cm\n• Jump 3: 200 cm\n• Jump 4: 240 cm\n• Jump 5: 280 cm",
      "Total distance = 120 + 160 + 200 + 240 + 280 = 1000 cm.",
      "1000 cm = 10 meters!"
    ],
    keyConcept: "In a sequence where each term increases by the same amount, add the common difference each time. Then add all terms!"
  },
  {
    id: 21,
    question: "⅙ hour + 2220 seconds - 12 minutes = ? minutes",
    options: [
      { label: "A", value: "35" },
      { label: "B", value: "59" },
      { label: "C", value: "183" },
      { label: "D", value: "192" }
    ],
    correctAnswer: "A",
    points: 4,
    hint: "Convert everything to minutes! ⅙ hour = 60 ÷ 6 = 10 minutes. 2220 seconds = 2220 ÷ 60 minutes.",
    explanation: [
      "Convert each part to minutes:\n• ⅙ hour = 60 ÷ 6 = 10 minutes",
      "• 2220 seconds = 2220 ÷ 60 = 37 minutes",
      "• 12 minutes = 12 minutes",
      "Now calculate: 10 + 37 - 12 = 35 minutes."
    ],
    keyConcept: "When adding or subtracting time, always convert to the SAME unit first! 1 hour = 60 minutes, 1 minute = 60 seconds."
  },
  {
    id: 22,
    question: "How many unit cubes are in this shape?\n\nThe shape has 3 layers:\n• Bottom layer: 5 cubes\n• Middle layer: 2 cubes\n• Top layer: 1 cube",
    options: [
      { label: "A", value: "5" },
      { label: "B", value: "6" },
      { label: "C", value: "8" },
      { label: "D", value: "9" }
    ],
    correctAnswer: "C",
    points: 4,
    hint: "Count the cubes in each layer and add them up. Don't forget the cubes you can't see — they support the ones on top!",
    explanation: [
      "Count cubes layer by layer:\n• Bottom layer: 5 cubes",
      "• Middle layer: 2 cubes (stacked on top of the bottom layer)",
      "• Top layer: 1 cube (stacked on top of the middle layer)",
      "Total cubes = 5 + 2 + 1 = 8 cubes."
    ],
    keyConcept: "When counting cubes in a 3D shape, count layer by layer from the bottom up. Remember hidden cubes that support the upper layers!"
  },
  {
    id: 23,
    question: "A cube net is shown with faces numbered: top row has 4, middle row has 2-5-6-1, bottom row has 3.\n\nWhich of the following CANNOT be obtained when the cube is folded?\n\nA) 4 on top, 2 and 6 on sides\nB) 5 on top, 2 and 6 on sides\nC) 2 on top, 6 and 5 on sides (with 2 and 6 next to each other)\nD) 4 on top, 5 and 3 on sides",
    options: [
      { label: "A", value: "Option A" },
      { label: "B", value: "Option B" },
      { label: "C", value: "Option C" },
      { label: "D", value: "Option D" }
    ],
    correctAnswer: "C",
    points: 5,
    hint: "When a cube net is folded, opposite faces cannot be next to each other. Find which faces are opposite first!",
    explanation: [
      "When folded, the opposite faces are:\n• 4 is opposite 3",
      "• 2 is opposite 6",
      "• 5 is opposite 1",
      "Option C says 2 and 6 are next to each other. But 2 and 6 are OPPOSITE faces! They can never be next to each other on a folded cube.",
      "So Option C is impossible!"
    ],
    keyConcept: "In a cube net, faces that are opposite in the net stay opposite when folded. Opposite faces can NEVER touch!"
  },
  {
    id: 24,
    question: "How much should be added to the largest 5-digit natural number to obtain the smallest 6-digit odd number?",
    options: [
      { label: "A", value: "2" },
      { label: "B", value: "11112" },
      { label: "C", value: "11111" },
      { label: "D", value: "1000" }
    ],
    correctAnswer: "A",
    points: 5,
    hint: "The largest 5-digit number is 99999. The smallest 6-digit number is 100000. But we need the smallest 6-digit ODD number...",
    explanation: [
      "Largest 5-digit number = 99999.",
      "Smallest 6-digit number = 100000.",
      "Smallest 6-digit ODD number = 100001 (because 100000 is even, so the next number is odd).",
      "Difference = 100001 - 99999 = 2."
    ],
    keyConcept: "The largest 5-digit number is 99999. The smallest 6-digit number is 100000. Odd numbers end in 1, 3, 5, 7, or 9!"
  },
  {
    id: 25,
    question: "A shop has green and purple notebooks. Some are lined and some are checkered. If there are 5108 green notebooks, 6864 lined notebooks, and 3004 purple lined notebooks, how many green checkered notebooks are there?",
    options: [
      { label: "A", value: "1248" },
      { label: "B", value: "1756" },
      { label: "C", value: "2104" },
      { label: "D", value: "3860" }
    ],
    correctAnswer: "A",
    points: 5,
    hint: "First find how many green lined notebooks there are. Total lined = green lined + purple lined. Then subtract from total green to find green checkered.",
    explanation: [
      "Step 1: Find green lined notebooks.\nTotal lined = 6864, purple lined = 3004.\nGreen lined = 6864 - 3004 = 3860.",
      "Step 2: Find green checkered notebooks.\nTotal green = 5108, green lined = 3860.\nGreen checkered = 5108 - 3860 = 1248."
    ],
    keyConcept: "Use a table or organize the information. Total = part + part. If you know the total and one part, subtract to find the other part!"
  },
  {
    id: 26,
    question: "There are 128 passengers on a bus. At the first stop, 24 board and 19 alight. At the second stop, 32 board and 13 alight. At the third stop, 18 board and 23 alight. How many passengers are on the bus at the end?",
    options: [
      { label: "A", value: "53" },
      { label: "B", value: "120" },
      { label: "C", value: "144" },
      { label: "D", value: "147" }
    ],
    correctAnswer: "D",
    points: 5,
    hint: "For each stop, calculate: boarded - alighted = change. Add all changes to the starting number. Or use a shortcut: (total boarded) - (total alighted) + starting.",
    explanation: [
      "Starting: 128 passengers.",
      "Stop 1: +24 - 19 = +5 → 128 + 5 = 133",
      "Stop 2: +32 - 13 = +19 → 133 + 19 = 152",
      "Stop 3: +18 - 23 = -5 → 152 - 5 = 147",
      "Final answer: 147 passengers!"
    ],
    keyConcept: "'Boarded' means people got ON (add). 'Alighted' means people got OFF (subtract). Track the running total at each stop!"
  },
  {
    id: 27,
    question: "On a farm, the number of ducks is 4 times the number of rabbits. The total number of legs of ducks and rabbits is 1404. How many rabbits are there?\n\n(Remember: ducks have 2 legs, rabbits have 4 legs)",
    options: [
      { label: "A", value: "107" },
      { label: "B", value: "117" },
      { label: "C", value: "123" },
      { label: "D", value: "132" }
    ],
    correctAnswer: "B",
    points: 6,
    hint: "If rabbits = R, then ducks = 4R. Rabbit legs = 4R, duck legs = 2 × 4R = 8R. Total legs = 4R + 8R = 12R = 1404.",
    explanation: [
      "Let R = number of rabbits.\nDucks = 4 × R = 4R.",
      "Rabbit legs: 4 × R = 4R.\nDuck legs: 2 × 4R = 8R.",
      "Total legs: 4R + 8R = 12R = 1404.",
      "R = 1404 ÷ 12 = 117 rabbits."
    ],
    keyConcept: "Use a letter for the unknown. Ducks have 2 legs, rabbits have 4 legs. Write an equation for total legs and solve!"
  },
  {
    id: 28,
    question: "My mother's age is 4 times my age. My grandfather's age is 3 times my mother's age. The sum of our ages is 136. How old is my grandfather?",
    options: [
      { label: "A", value: "72" },
      { label: "B", value: "84" },
      { label: "C", value: "96" },
      { label: "D", value: "98" }
    ],
    correctAnswer: "C",
    points: 6,
    hint: "If my age is x, mother's age is 4x, and grandfather's age is 3 × 4x = 12x. All three add to 136. So x + 4x + 12x = 136.",
    explanation: [
      "Let my age = x.\nMother's age = 4x.\nGrandfather's age = 3 × 4x = 12x.",
      "Sum: x + 4x + 12x = 17x = 136.",
      "x = 136 ÷ 17 = 8.",
      "Grandfather's age = 12 × 8 = 96 years old!"
    ],
    keyConcept: "When you have 'times' relationships, use one letter for the smallest amount. Then everything else is a multiple of that letter!"
  },
  {
    id: 29,
    question: "What is ¹/₁₇ of a number, given that ⁶/₁₄ of the number is 102?",
    options: [
      { label: "A", value: "8" },
      { label: "B", value: "10" },
      { label: "C", value: "14" },
      { label: "D", value: "17" }
    ],
    correctAnswer: "C",
    points: 6,
    hint: "First simplify ⁶/₁₄ = ³/₇. If ³/₇ of the number is 102, find the whole number first, then find ¹/₁₇ of it.",
    explanation: [
      "Simplify ⁶/₁₄ = ³/₇.",
      "If ³/₇ of the number = 102, then ¹/₇ of the number = 102 ÷ 3 = 34.",
      "The whole number = 34 × 7 = 238.",
      "Now find ¹/₁₇ of 238: 238 ÷ 17 = 14."
    ],
    keyConcept: "'Of' means multiply in fractions. If a fraction of a number is given, divide by the numerator to find 1 part, then multiply by the denominator!"
  },
  {
    id: 30,
    question: "A flower has leaves with numbers: 126, 504, 378, 1022. Each number will be divided by 14. The leaf with a number that does NOT give a two-digit result will be torn off. Which leaf is torn off?",
    options: [
      { label: "A", value: "126" },
      { label: "B", value: "504" },
      { label: "C", value: "378" },
      { label: "D", value: "1022" }
    ],
    correctAnswer: "A",
    points: 6,
    hint: "Divide each number by 14. A two-digit result is between 10 and 99. Which division gives a single-digit answer?",
    explanation: [
      "Divide each number by 14:\n• 126 ÷ 14 = 9 (one digit — NOT two digits!)",
      "• 504 ÷ 14 = 36 (two digits ✓)",
      "• 378 ÷ 14 = 27 (two digits ✓)",
      "• 1022 ÷ 14 = 73 (two digits ✓)",
      "Only 126 ÷ 14 = 9 gives a one-digit result. So the leaf with 126 is torn off!"
    ],
    keyConcept: "A two-digit number is from 10 to 99. If division gives a result less than 10, it's a single-digit number!"
  },
  {
    id: 31,
    question: "A cube has six faces with pictures: Smiley, Star, Flower, Teacup, Ladybug, and Crayon. From the cube's net diagram, which faces are opposite each other?\n\nThe answer is:\n• Smiley opposite Crayon\n• Star opposite Teacup\n• Flower opposite Ladybug",
    options: [
      { label: "A", value: "Smiley-Star, Flower-Teacup, Ladybug-Crayon" },
      { label: "B", value: "Smiley-Crayon, Star-Teacup, Flower-Ladybug" },
      { label: "C", value: "Smiley-Flower, Star-Ladybug, Teacup-Crayon" },
      { label: "D", value: "Smiley-Teacup, Star-Crayon, Flower-Ladybug" }
    ],
    correctAnswer: "B",
    points: 7,
    hint: "In a cube net, faces that are separated by one face in a straight line are usually opposite. The top and bottom of the net fold to be opposite.",
    explanation: [
      "When you fold the cube net:\n• The top face (Smiley) folds down to be opposite the bottom face (Crayon).",
      "• The middle row wraps around, so Star and Teacup end up opposite.",
      "• Flower and Ladybug are opposite.",
      "The correct pairs are: Smiley-Crayon, Star-Teacup, Flower-Ladybug."
    ],
    keyConcept: "In a cube net, opposite faces are never next to each other. The top and bottom of the net are always opposite when folded!"
  },
  {
    id: 32,
    question: "A pattern uses triangles:\n• Step 1: 7 triangles\n• Step 2: 10 triangles\n• Step 3: 13 triangles\n• Each step adds 3 more triangles\n\nIn which step are there 31 triangles?",
    options: [
      { label: "A", value: "Step 8" },
      { label: "B", value: "Step 9" },
      { label: "C", value: "Step 10" },
      { label: "D", value: "Step 11" }
    ],
    correctAnswer: "B",
    points: 7,
    hint: "The formula is: triangles = 7 + 3 × (step - 1). Set this equal to 31 and solve for the step number!",
    explanation: [
      "The pattern formula is:\ntriangles = 7 + 3 × (step - 1)",
      "Set equal to 31:\n7 + 3 × (step - 1) = 31",
      "3 × (step - 1) = 24",
      "step - 1 = 8",
      "step = 9"
    ],
    keyConcept: "In a pattern that adds the same amount each time, the formula is: start + difference × (step - 1). Work backwards to find the step!"
  },
  {
    id: 33,
    question: "Three overlapping circles each contain 5 numbers. The sum of numbers in each circle is 60.\n\nCircle 1: 15, 8, 9, tree, flower\nCircle 2: tree, flower, 7, 15, sun\nCircle 3: 15, 12, 6, star, sun\n\nWhat number should be in the box marked with a star?",
    options: [
      { label: "A", value: "17" },
      { label: "B", value: "19" },
      { label: "C", value: "27" },
      { label: "D", value: "29" }
    ],
    correctAnswer: "A",
    points: 7,
    hint: "From Circle 1, find tree + flower. Use that in Circle 2 to find 'sun'. Then use 'sun' in Circle 3 to find the star!",
    explanation: [
      "Circle 1: 15 + 8 + 9 + tree + flower = 60.\nSo tree + flower = 60 - 32 = 28.",
      "Circle 2: tree + flower + 7 + 15 + sun = 60.\n28 + 22 + sun = 60.\nsun = 10.",
      "Circle 3: 15 + 12 + 6 + star + sun = 60.\n33 + star + 10 = 60.\nstar = 17!"
    ],
    keyConcept: "In overlapping circle puzzles, find what the overlapping regions equal first, then use that to find other values!"
  },
  {
    id: 34,
    question: "Two scales are balanced:\n\nScale I: 1 cuboid + 1 cylinder + 2 pyramids = 3 cylinders\nScale II: 1 cuboid + 1 cylinder = 1 cuboid + 3 pyramids\n\nIn Scale III: 1 cuboid + 1 cylinder = ? pyramids",
    options: [
      { label: "A", value: "5" },
      { label: "B", value: "6" },
      { label: "C", value: "7" },
      { label: "D", value: "11" }
    ],
    correctAnswer: "C",
    points: 7,
    hint: "From Scale II: if cuboid + cylinder = cuboid + 3 pyramids, then 1 cylinder = 3 pyramids. From Scale I, replace cylinder with pyramids to find cuboid in terms of pyramids.",
    explanation: [
      "From Scale II: cuboid + cylinder = cuboid + 3 pyramids.\nSubtract cuboid from both sides: 1 cylinder = 3 pyramids.",
      "From Scale I: cuboid + cylinder + 2 pyramids = 3 cylinders.\nReplace cylinder with 3 pyramids:\ncuboid + 3 + 2 = 9 pyramids.\ncuboid = 4 pyramids.",
      "Scale III: cuboid + cylinder = 4 + 3 = 7 pyramids!"
    ],
    keyConcept: "In balance puzzles, you can 'cancel' the same thing from both sides. Then substitute to find what one shape equals!"
  },
  {
    id: 35,
    question: "Find the missing piece that fits into the empty space in the picture. The empty space is L-shaped.",
    options: [
      { label: "A", value: "Piece A (L-shaped, correct orientation)" },
      { label: "B", value: "Piece B (L-shaped but wrong proportions)" },
      { label: "C", value: "Piece C (L-shaped but wrong orientation)" },
      { label: "D", value: "Piece D (L-shaped but wrong orientation)" }
    ],
    correctAnswer: "A",
    points: 7,
    hint: "Look at the empty space carefully. Notice its L-shape and which direction the L points. Match the shape AND orientation!",
    explanation: [
      "The empty space has a specific L-shape with one part extending horizontally and another vertically.",
      "Option A matches both the shape AND the orientation needed to fit perfectly.",
      "The other options are either L-shaped but with wrong orientation or wrong proportions.",
      "The answer is Piece A!"
    ],
    keyConcept: "When finding a missing puzzle piece, check BOTH the shape AND the orientation. It must fit perfectly!"
  }
];
