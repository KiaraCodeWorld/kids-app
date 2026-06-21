"""
Daily Discovery module content.
Each entry: {id, category, title, emoji, teaser, body, challenge, tag}
Categories: space | manners | funfact | hack | game | trending | news
News items are LLM-generated at runtime; other categories use this static pool.
"""
import random
from datetime import date


def _d(id, cat, emoji, title, teaser, body, challenge, tag=''):
    return dict(id=id, category=cat, emoji=emoji, title=title,
                teaser=teaser, body=body, challenge=challenge, tag=tag)


# ── SPACE ─────────────────────────────────────────────────────────────────────
SPACE = [
_d('sp001','space','🌌','Black Holes Eat Light',
   'Nothing — not even light — can escape a black hole.',
   'A black hole forms when a massive star collapses under its own gravity. The gravity becomes so strong that the escape velocity exceeds the speed of light — 299,792 km/s. Not a single photon can get out. The boundary of no return is called the **event horizon**. Scientists photographed one for the first time in 2019 — it took a telescope the size of Earth to do it.',
   'If our Sun became a black hole (it won\'t!), how wide would it be? Look it up!',
   'Mind-Bending'),

_d('sp002','space','☀️','The Sun Is a Giant Nuclear Reactor',
   'Every second the Sun fuses 600 million tons of hydrogen into helium.',
   'Deep in the Sun\'s core, temperatures hit 15 million°C — hot enough to force hydrogen atoms to fuse together. This fusion releases enormous energy as light and heat. The light takes about **8 minutes** to travel 150 million km to reach Earth. But inside the Sun, that same energy bounces around for up to 100,000 years before escaping!',
   'How many Earths could fit inside the Sun? (Hint: it\'s over a million!)',
   'Science'),

_d('sp003','space','🪐','Saturn\'s Rings Are Mostly Ice',
   'Saturn\'s spectacular rings are made of billions of ice chunks and rocks.',
   'Saturn\'s rings stretch up to 282,000 km wide — almost the distance from Earth to the Moon — yet they are only about 10 to 100 metres thick. They are made of water ice, from dust-sized particles to chunks as big as houses. Scientists think the rings formed relatively recently in cosmic terms — perhaps only 100 million years ago when a moon was destroyed.',
   'Which planet has the most moons in our solar system? You might be surprised!',
   'Wow'),

_d('sp004','space','🌙','The Moon Is Moving Away From Earth',
   'Every year the Moon drifts about 3.8 cm further from Earth.',
   'The Moon was formed about 4.5 billion years ago, likely when a Mars-sized object crashed into early Earth. Back then it was 14 times closer than it is today. Tidal forces from Earth\'s oceans gradually slow Earth\'s rotation and push the Moon outward. In about 50 billion years — long after the Sun dies — the Moon would finally stop receding.',
   'If the Moon were closer, what would be different about life on Earth?',
   'Deep Think'),

_d('sp005','space','🚀','Voyager 1 Has Left the Solar System',
   'Launched in 1977, Voyager 1 is now over 23 billion km from Earth.',
   'Voyager 1 is the farthest human-made object ever. It crossed into **interstellar space** — the space between stars — in 2012. It still sends data back to Earth, but the signal takes over 22 hours to arrive travelling at the speed of light. Its power comes from decaying plutonium. Scientists estimate it will keep sending signals until around 2025.',
   'How long would it take a modern rocket to reach Voyager 1?',
   'Record Breaker'),

_d('sp006','space','🌠','Stars Are Born in Nebulae',
   'Giant clouds of gas and dust are the nurseries where new stars form.',
   'A nebula is a vast cloud of hydrogen gas and dust in space. When part of it clumps together under gravity, it begins to spin and heat up. After millions of years it becomes hot enough to trigger nuclear fusion — and a new star is born. The Orion Nebula, visible to the naked eye, is one of the nearest and most active star-forming regions — 1,344 light-years away.',
   'Find the Orion Nebula in the night sky tonight using a star map app.',
   'Explorer'),

_d('sp007','space','🌍','Earth\'s Magnetic Field Is Our Shield',
   'Without Earth\'s magnetic field, solar winds would strip away our atmosphere.',
   'Earth\'s core generates a magnetic field that wraps around the planet like an invisible bubble — the **magnetosphere**. It deflects charged particles from the Sun called solar wind. Without it, those particles would slowly erode our atmosphere, as happened to Mars billions of years ago. The Northern and Southern Lights (auroras) are what happens when particles sneak through near the poles.',
   'What would happen to satellites and GPS if Earth lost its magnetic field?',
   'Essential'),

_d('sp008','space','🔭','James Webb Telescope Sees the Past',
   'The JWST is so powerful it can see galaxies that formed just 300 million years after the Big Bang.',
   'Light takes time to travel. When you look at a star 100 light-years away, you see it as it was 100 years ago. The James Webb Space Telescope, launched in 2021, can detect infrared light from galaxies over 13 billion light-years away — meaning we are literally seeing the early universe. Its primary mirror is 6.5 metres wide and must operate at -233°C to function.',
   'What is the oldest thing the JWST has photographed so far? Research it!',
   'Technology'),

_d('sp009','space','💫','Neutron Stars Are Impossibly Dense',
   'A teaspoon of neutron star material would weigh about a billion tons.',
   'When a star between 8 and 20 times the Sun\'s mass explodes as a supernova, its core can collapse into a **neutron star** — an object about 20 km across but containing more mass than our Sun. Neutron stars spin incredibly fast — some rotate 700 times per second. These are called pulsars, and they beam radio waves like a lighthouse.',
   'If you weighed a teaspoon of neutron star material on Earth, how much would it weigh?',
   'Mind-Bending'),

_d('sp010','space','🪐','Mars Has the Tallest Volcano in the Solar System',
   'Olympus Mons on Mars is nearly three times the height of Mount Everest.',
   'Olympus Mons stands 21.9 km above the Martian surface — Mount Everest is only 8.8 km. It is so wide (600 km across) that if you stood at its base, the peak would be beyond the horizon. It is a **shield volcano**, built up gradually by flowing lava. Because Mars has no tectonic plates to move the crust, lava kept piling up at one spot for billions of years.',
   'Compare Olympus Mons to the largest volcano on Earth. What is the difference?',
   'Record Breaker'),

_d('sp011','space','🌌','The Universe Is Expanding Faster and Faster',
   'The universe is not just expanding — it is accelerating.',
   'Since the Big Bang 13.8 billion years ago, the universe has been expanding. But in 1998 scientists discovered the expansion is **speeding up** — driven by a mysterious force called **dark energy** that makes up about 68% of the universe. Nobody fully understands what dark energy is. The farther away a galaxy is, the faster it is receding from us.',
   'If the universe keeps accelerating, what will eventually happen to the night sky?',
   'Mystery'),

_d('sp012','space','🛸','There Are More Stars Than Grains of Sand on Earth',
   'The observable universe contains around 2 trillion galaxies.',
   'Each galaxy contains hundreds of billions of stars. The Milky Way alone has an estimated 200–400 billion stars. Scientists estimate there are more stars in the observable universe than all the grains of sand on every beach and desert on Earth combined. The number is roughly 10²⁴ — that is a 1 with 24 zeros after it.',
   'Try to write the number 10²⁴ in full. How long does it take?',
   'Scale'),

_d('sp013','space','🌞','Space Is Completely Silent',
   'In space, no one can hear you scream — and that is literally true.',
   'Sound is a vibration that travels through matter — air, water, or solid objects. Space is nearly a perfect vacuum, with almost no particles to carry vibrations. So explosions, rockets, and even stars make no sound in space. Astronauts communicate through radio waves, which are electromagnetic — not mechanical — and can travel through a vacuum.',
   'How do astronauts on the ISS talk to each other inside and outside the station?',
   'Physics'),

_d('sp014','space','🧲','One Day on Venus Is Longer Than Its Year',
   'Venus rotates so slowly that it completes an orbit around the Sun before one full rotation.',
   'Venus takes 243 Earth days to rotate once on its axis, but only 225 days to orbit the Sun. So a day on Venus is longer than its year! To make it weirder, Venus spins backwards — if you were on Venus, the Sun would rise in the west and set in the east. Its surface temperature is 465°C — hotter than Mercury — due to a runaway greenhouse effect.',
   'Make a list of three ways a day on Venus would be different from a day on Earth.',
   'Weird Science'),

_d('sp015','space','🌊','Europa May Have a Hidden Ocean',
   'Jupiter\'s moon Europa might hold more liquid water than all of Earth\'s oceans.',
   'Europa, one of Jupiter\'s 95 moons, is covered in a thick layer of ice. But scientists believe beneath that ice lies a vast liquid ocean, kept warm by tidal heating from Jupiter\'s gravity. Where there is liquid water, there could be life. NASA\'s Europa Clipper mission, launched in 2024, is heading there to investigate. It arrives around 2030.',
   'What conditions are needed for life as we know it? Does Europa have them?',
   'Life?'),

_d('sp016','space','☄️','Shooting Stars Are Not Actually Stars',
   'A shooting star is a tiny piece of space rock burning up in Earth\'s atmosphere.',
   'What we call shooting stars are really **meteors** — small bits of dust and rock from comets or asteroids. When they enter Earth\'s atmosphere at high speed, friction heats them until they glow brightly. Most meteors are no bigger than a grain of sand. Meteor showers happen when Earth passes through a trail of debris left by a comet. The Perseids in August are one of the best shows, with up to 100 meteors per hour.',
   'Find out when the next meteor shower is and plan a night to watch it.',
   'Sky Watch'),

_d('sp017','space','🔴','Mars Is Red Because It Is Rusty',
   'The Red Planet gets its color from iron oxide — the same stuff that makes rust red.',
   'Mars\'s surface is covered in iron minerals that reacted with oxygen over billions of years, creating rust-like dust. This dust is so fine that storms can wrap the entire planet in a red haze. Beneath the dusty surface, Mars has volcanoes, canyons, and polar ice caps made of frozen water and carbon dioxide. Future missions hope to turn some of that ice into drinking water and rocket fuel.',
   'Design a Mars habitat. What three things would you absolutely need to bring?'),

_d('sp018','space','🌑','Humans Could Live on the Moon Sooner Than You Think',
   'NASA\'s Artemis program plans to send astronauts back to the Moon by the late 2020s.',
   'The Moon is only 384,400 km away — close enough to travel in about 3 days. Future astronauts may live in **lunar bases** built inside craters or lava tubes for protection from radiation. They would mine ice at the south pole for water and oxygen. Living on the Moon is also seen as practice for eventual missions to Mars, which is much farther and harder to reach.',
   'Would you rather spend a month in a Moon base or a year in Antarctica? Why?'),

_d('sp019','space','🌪️','Jupiter Spins Faster Than Any Other Planet',
   'A day on Jupiter lasts only about 10 hours — the shortest of all the planets.',
   'Jupiter is the largest planet in our solar system, but it spins incredibly fast. This rapid rotation stretches its clouds into the famous horizontal bands. The fast spin also creates strong storms, including the Great Red Spot — a storm bigger than Earth that has lasted for centuries. Jupiter has at least 95 moons, including Ganymede, the largest moon in the solar system.',
   'If Earth had 10-hour days, how would your school schedule change?'),

_d('sp020','space','🪐','Exoplanets Are Worlds Beyond Our Solar System',
   'Scientists have discovered more than 5,500 planets orbiting other stars.',
   'These alien worlds are called **exoplanets**. Some are giant gas planets like Jupiter; others are rocky like Earth. The **habitable zone** is the right distance from a star where liquid water could exist. Telescopes like Kepler and TESS hunt for exoplanets by watching stars dim slightly as planets pass in front of them. The James Webb Space Telescope is now studying their atmospheres for signs of water or life.',
   'If you discovered an Earth-like planet, what would you name it?'),
]

# ── TABLE MANNERS & LIFE ETIQUETTE ───────────────────────────────────────────
MANNERS = [
_d('mn001','manners','🍽️','The Fork Goes on the Left',
   'There is a simple system to table setting — and it only takes 30 seconds to learn.',
   'The basic rule: **fork on the left, knife and spoon on the right**. The knife blade faces inward (toward the plate). If there are multiple forks, the salad fork is outermost — you work from the outside in. Napkin goes on the lap the moment you sit. These conventions come from European dining tradition and are used at formal settings worldwide.',
   'Set a full dinner table correctly from memory. Time yourself!',
   'Life Skill'),

_d('mn002','manners','📱','Phones Away at the Table',
   'Checking your phone during a meal sends a clear signal: they are less important than your screen.',
   'Research from the University of Essex found that even having a phone visible on a table — not being used — reduces the quality of a conversation. People feel less connected and share less. "Phone stacking" (everyone puts phones face-down in a pile) is one solution. The first person to touch theirs pays the bill — or does the dishes.',
   'Try one full meal with zero phone access. How did the conversation change?',
   'Social Intelligence'),

_d('mn003','manners','🗣️','Don\'t Talk With Your Mouth Full',
   'It is rude, it is hard to understand, and it risks a choking hazard.',
   'This is one of the oldest table manner rules — and the reason is straightforward. Chewing with an open mouth is unpleasant to watch and hear, talking while chewing makes speech unclear, and it can send food to the wrong place. The simple habit: finish chewing, swallow, then speak. It also slows you down and improves digestion.',
   'For one meal, pause before speaking until your mouth is completely clear. Notice how it changes your eating pace.',
   'Classic'),

_d('mn004','manners','🙏','Always Say Please and Thank You',
   'Two words that cost nothing and change everything about how people see you.',
   '"Please" and "thank you" are called **magic words** for good reason. Studies show people who use them regularly are perceived as more trustworthy, likeable, and intelligent. In professional settings, gratitude increases cooperation by up to 50% according to research. Different cultures have their own equivalents — learning them in another language is an instant sign of respect.',
   'Say a genuine "thank you" to three different people today — and mean it.',
   'Power Habit'),

_d('mn005','manners','🚪','Hold the Door Open',
   'A two-second gesture that signals you notice other people exist.',
   'Holding a door for the person behind you is one of the simplest acts of everyday courtesy. It costs nothing. But failing to do it — letting a door swing into someone — makes an immediate negative impression. The rule: if someone is within about 3–4 steps of the door, hold it. Eye contact and a smile complete it.',
   'Count how many times today you hold a door or someone holds one for you.',
   'Everyday'),

_d('mn006','manners','✉️','How to Write a Proper Thank You Note',
   'A handwritten note is the single most impressive social gesture almost no one does anymore.',
   'Structure: **1.** State what you are thanking them for specifically. **2.** Describe why it mattered to you. **3.** Mention the future ("I look forward to seeing you" or "I\'ll use this often"). Sign with warmth. It does not need to be long — five sentences is plenty. A handwritten note beats a text in every study of perceived gratitude.',
   'Write a thank you note to someone who helped you recently. Actually send it.',
   'Underrated'),

_d('mn007','manners','👂','Listen Without Interrupting',
   'The most underrated social skill: letting someone finish their sentence.',
   'Studies show most people start formulating their reply before the speaker has finished. This means they stop truly listening midway. Interrupting — even with enthusiasm — signals that your words matter more than theirs. The fix: wait one full second after someone finishes before you speak. You will be surprised how often they have more to say.',
   'In your next conversation, count silently to one before responding every time.',
   'Social Intelligence'),

_d('mn008','manners','🧂','Pass the Salt and Pepper Together',
   'If someone asks for the salt, always pass the pepper too — they are a pair.',
   'This is a classic dining rule most people do not know. The salt and pepper are considered a set — passing one alone is considered poor form at a formal dinner. You also should not season your food before tasting it — it suggests you have already decided the cook got it wrong. Reach and pass food around the table; never reach across someone.',
   'Next meal: research one table etiquette rule from a different culture (Japan, India, or France).',
   'Dinner Wisdom'),

_d('mn009','manners','🤝','The Right Way to Shake Hands',
   'A good handshake takes less than three seconds and makes a lasting impression.',
   'A proper handshake: web-to-web contact (the skin between thumb and index finger meets the other person\'s). Firm but not crushing. Two to three pumps. Eye contact and a smile. A limp handshake signals low confidence; too hard signals aggression. Practice until it is natural — in job interviews and first meetings, a handshake is often the most-remembered moment.',
   'Practice a proper handshake with a family member and ask for honest feedback.',
   'Life Skill'),

_d('mn010','manners','🎤','How to Introduce People Properly',
   'Good introductions make everyone comfortable — bad ones create awkward silence.',
   'When introducing two people, **say both names**, add a connecting detail: "This is Maya — she runs the robotics club. And this is Dev, who loves science fiction." The detail gives people an instant conversation starter. In formal settings, introduce the junior person to the senior person: "Dr. Patel, this is my classmate Arjun."',
   'Introduce two people in your life to each other — use the full technique.',
   'Social Power'),

_d('mn011','manners','🧹','Clean Up After Yourself',
   'Leaving a space better than you found it is one of the highest-value habits.',
   'Whether it\'s a cafeteria table, a library desk, or a friend\'s home — leaving things clean shows awareness of other people\'s experience. In Japan, students clean their own classrooms daily — research suggests it builds ownership, pride, and respect for shared spaces. Clean-up also reduces stress: a messy environment raises cortisol (the stress hormone).',
   'Clean one shared space today that you did not make messy.',
   'High Value'),

_d('mn012','manners','🗣️','Apologize Properly When You Are Wrong',
   'A real apology has three parts — most people only do one.',
   '**1. Acknowledge** what you did: "I forgot to tell you about the change in plans." **2. Take responsibility** without excuses: "That was careless of me." **3. Offer repair**: "What can I do to make it right?" The most common mistake is adding "but" — which cancels the apology. "I\'m sorry BUT..." shifts blame back to the other person.',
   'Think of a time you owe someone a real apology. Use the three-part formula.',
   'Relationships'),

_d('mn013','manners','🌍','Table Manners Around the World',
   'Burping in some countries is a compliment. Finishing your plate in others is an insult.',
   'In **China**: slurping noodles shows appreciation. In **Japan**: pouring your own drink is considered rude — pour for others first. In **Ethiopia**: eating from each other\'s plates (gursha) is a sign of love. In **France**: bread goes directly on the tablecloth, not a bread plate. What is polite varies wildly — awareness is the key to being a respectful guest anywhere.',
   'Pick one country and research three of their dining etiquette rules.',
   'Global'),

_d('mn014','manners','🧠','The Difference Between Being Polite and Being Kind',
   'Politeness follows rules. Kindness comes from caring. Both matter — for different reasons.',
   'Politeness is the social code — saying "please," arriving on time, not talking with your mouth full. It signals that you respect social norms. Kindness is internal — it comes from genuinely caring about other people\'s feelings. You can be polite without being kind (technically following rules while being cold). The goal is both: follow the code AND mean it.',
   'Find one moment today to be kind beyond what politeness requires.',
   'Deep Think'),

_d('mn015','manners','💬','How to Disagree Without Being Rude',
   'You can be completely honest and completely respectful at the same time.',
   'The framework: **1.** Acknowledge their point first — "I see why you think that." **2.** Use "I" language — "I see it differently" not "You\'re wrong." **3.** Give your reason calmly. **4.** End with curiosity — "What makes you see it that way?" This signals confidence and respect simultaneously. It is also far more persuasive than arguing.',
   'Next time you disagree with someone, use all four steps.',
   'Communication'),

_d('mn016','manners','🚶','Say "Excuse Me" When You Need to Pass',
   'Two small words make crowded hallways, buses, and rooms much more pleasant.',
   'Saying "excuse me" acknowledges that you are briefly interrupting someone\'s space. It works when you need to walk between people, get someone\'s attention, or leave a conversation politely. Pair it with a soft touch on the shoulder if appropriate and make eye contact. This habit signals awareness and respect in busy public places.',
   'Count how many times you say "excuse me" today. Did people respond politely?'),

_d('mn017','manners','🍕','The Art of Sharing Food Fairly',
   'Splitting a pizza or snacks fairly is a small test of generosity and math.',
   'When sharing food, offer the first piece to someone else. If you are cutting, aim for equal portions. If there is one last piece, offer it around before taking it. In many cultures, refusing food first is polite — hosts may insist. Sharing food builds trust and connection, and being fair about it prevents arguments before they start.',
   'Next time you share a snack, make sure everyone gets a fair portion.'),

_d('mn018','manners','📩','Always RSVP to Invitations',
   'RSVP stands for "Répondez s\'il vous plaît" — French for "please respond."',
   'When someone invites you to a party or event, they need to know how many people are coming for food, seats, and planning. Responding promptly — even to say no — shows respect for the host\'s effort. A simple text or note works: "Thanks for inviting me. I\'d love to come!" or "I can\'t make it, but I hope it\'s wonderful."',
   'Practice writing a polite RSVP for a pretend party invitation.'),

_d('mn019','manners','👀','Do Not Point or Stare at Others',
   'Pointing and staring can make people feel uncomfortable or judged.',
   'It is natural to notice differences, but staring sends a message that someone is being watched or singled out. If you have a question, ask a trusted adult privately later. Similarly, pointing at people can feel accusatory. Instead, use open hand gestures or describe directions with words. This small habit helps everyone feel more comfortable in public.',
   'Notice today: when do you feel the urge to stare? Practice looking away gently.'),

_d('mn020','manners','🙌','Thank People Who Serve You',
   'Bus drivers, cashiers, cleaners, and servers make daily life run smoothly.',
   'A sincere "thank you" to someone helping you costs nothing but can improve their whole day. Make eye contact, smile, and use their name if they are wearing a name tag. Gratitude toward service workers teaches you to notice the effort behind everyday conveniences and treats every person with dignity.',
   'Thank three people who help you today — a driver, a server, a cleaner, or a teacher.'),
]

# ── FUN FACTS ─────────────────────────────────────────────────────────────────
FUNFACTS = [
_d('ff001','funfact','🐙','Octopuses Have Three Hearts and Blue Blood',
   'And all three hearts stop beating when an octopus swims.',
   'Octopuses have **three hearts**: two pump blood to the gills, one pumps it to the body. Their blood is blue because it uses copper-based hemocyanin instead of iron-based hemoglobin. When they swim, the main heart stops, which is why they prefer crawling — swimming exhausts them quickly. They also have nine brains: one central brain and one in each of their eight arms.',
   'If you had one brain in each arm, what would your eight arms each decide to do right now?',
   'Animal Kingdom'),

_d('ff002','funfact','🍯','Honey Never Expires',
   'Archaeologists found 3,000-year-old honey in Egyptian tombs — still edible.',
   'Honey\'s chemistry makes it naturally antimicrobial. It is very low in moisture (water activity below 0.6), highly acidic (pH 3.2–4.5), and contains hydrogen peroxide produced by the enzyme glucose oxidase. Bacteria and microorganisms need water to survive — honey starves them. As long as it is sealed and kept from moisture, it will last indefinitely.',
   'What other foods have extremely long shelf lives? Research the top five.',
   'Chemistry'),

_d('ff003','funfact','🦈','Sharks Are Older Than Trees',
   'Sharks have existed for 450 million years — trees evolved only 385 million years ago.',
   'Sharks predate trees, dinosaurs, and even most complex land life. They survived all five mass extinctions, including the one that wiped out the dinosaurs. The coelacanth — a fish thought to be extinct — was found alive in 1938, unchanged for 400 million years. Sharks have barely needed to evolve because they are already a nearly perfect predator design.',
   'Name one other animal that predates dinosaurs.',
   'Ancient Life'),

_d('ff004','funfact','🧠','Your Brain Generates Enough Electricity to Power a Lightbulb',
   'The human brain produces about 20 watts of electricity — enough to light a dim bulb.',
   'Your brain has about 86 billion neurons, each connected to up to 10,000 others. When neurons fire, they generate tiny electrical pulses. Together they produce measurable electrical activity — about 20 watts during an active day. An EEG machine can detect these signals through the scalp. Scientists can now use AI to decode brain signals into words for people who cannot speak.',
   'If your brain ran on electricity like a device, how would that change medicine?',
   'Body Science'),

_d('ff005','funfact','🦋','Butterflies Taste With Their Feet',
   'Butterflies have taste sensors on their legs — they taste everything they land on.',
   'Butterflies have chemoreceptors on their tarsi (feet) that are 200 times more sensitive than the human tongue. The moment a butterfly lands on a leaf, it instantly tastes whether the plant is suitable for laying eggs. Caterpillars can only eat certain plants — monarch butterflies, for example, only lay eggs on milkweed. The feet-tasting helps them find the right plant instantly.',
   'What would it be like to taste everything you touched? Write three sentences about it.',
   'Biology'),

_d('ff006','funfact','🌊','The Ocean Produces Over Half of Earth\'s Oxygen',
   'More than half the oxygen you breathe right now came from the ocean, not trees.',
   'Phytoplankton — microscopic plant-like organisms in the ocean — produce 50–85% of Earth\'s oxygen through photosynthesis. The most common, Prochlorococcus, is less than 1 micron wide but may be the most abundant photosynthetic organism on Earth. If ocean temperatures rise too much, phytoplankton die — threatening the oxygen supply of all air-breathing life on Earth.',
   'Why is ocean health directly connected to air quality on land?',
   'Environment'),

_d('ff007','funfact','🦦','Sea Otters Hold Hands While Sleeping',
   'To keep from drifting apart in currents, sea otters hold hands in groups called rafts.',
   'Sea otters spend most of their lives floating in the ocean. Groups — called **rafts** — can contain hundreds of otters. To stop the current from separating them while they sleep, they wrap themselves in kelp or hold each other\'s paws. Sea otters also have the densest fur of any mammal — up to 1 million hairs per square inch — which keeps them warm without blubber.',
   'Sea otters are a keystone species. Find out what that means and why it matters.',
   'Adorable Science'),

_d('ff008','funfact','🔢','There Are More Possible Chess Games Than Atoms in the Universe',
   'The number of possible chess games is estimated at 10¹²⁰ — more than atoms in the observable universe.',
   'There are about 10⁸⁰ atoms in the observable universe. But the number of possible chess games — called the **Shannon Number** — is estimated at 10¹²⁰. That is why even the most powerful AI cannot "solve" chess by brute force. IBM\'s Deep Blue beat Garry Kasparov in 1997 using selective search, not by calculating every possibility. Today\'s AI engines are even smarter.',
   'If every computer on Earth calculated one game per nanosecond, how long to check every chess game?',
   'Math Magic'),

_d('ff009','funfact','🐘','Elephants Are the Only Animals That Cannot Jump',
   'Every other mammal on Earth can jump — elephants physically cannot.',
   'Elephants\' weight (up to 7,000 kg for African males) and bone structure make jumping physically impossible. Their leg bones point straight down — they cannot crouch or spring. They also never have all four feet off the ground simultaneously, even when running. However they can run at up to 25 km/h. Their trunks contain 40,000 muscles and can lift 270 kg.',
   'What other physical abilities do elephants have that most animals cannot match?',
   'Animal Limits'),

_d('ff010','funfact','🌡️','Hot Water Can Freeze Faster Than Cold Water',
   'This real phenomenon is called the Mpemba Effect — and scientists still debate why.',
   'In 1963, a Tanzanian student named Erasto Mpemba noticed that hot ice cream mix froze faster than cold mix. Scientists confirmed the phenomenon but still argue about the exact mechanism. Leading theories involve evaporation (hot water loses mass), dissolved gases, convection currents, or hydrogen bond restructuring. It does not always happen — the conditions matter.',
   'Try the Mpemba Effect at home: freeze hot and cold water at the same time. Which freezes first?',
   'Experiment'),

_d('ff011','funfact','🦎','A Day Has 86,400 Seconds — But It Is Getting Longer',
   'Earth\'s rotation is gradually slowing — meaning days are getting longer over millions of years.',
   'When Earth formed, a day was only about 6 hours long. The Moon\'s tidal forces are gradually slowing Earth\'s spin. Currently, days are getting longer by about 1.4 milliseconds per century. When dinosaurs lived, a day was about 23 hours. In the very distant future, a day could last months. This same tidal locking is why we always see the same face of the Moon.',
   'If a day were 30 hours long, how would school and sleep schedules change?',
   'Time Science'),

_d('ff012','funfact','🌿','Cleopatra Lived Closer in Time to the Moon Landing Than to the Building of the Great Pyramid',
   'The Great Pyramid is 4,500 years old. Cleopatra lived 2,000 years ago. The Moon landing was 55 years ago.',
   'This is one of the most mind-bending timeline facts in history. The Great Pyramid of Giza was completed around 2560 BC. Cleopatra was born around 69 BC — roughly 2,500 years after the pyramid was built. But she lived only about 2,000 years before us. The Apollo 11 Moon landing was 1969. So Cleopatra is closer to us on the timeline than to the pyramid builders.',
   'Find one other "closer than you think" timeline fact from history.',
   'History Mind-Bend'),

_d('ff013','funfact','🧊','There Is a Cloud in Space That Contains Enough Alcohol to Fill Earth\'s Oceans 10,000 Times',
   'The Sagittarius B2 cloud near the center of our galaxy contains a vast amount of ethanol.',
   'Molecular cloud Sagittarius B2, about 26,000 light-years from Earth, contains billions of litres of ethyl alcohol (the kind in drinks) along with other organic molecules. Space is full of complex chemistry — amino acids, sugars, and alcohols have been found in meteorites and interstellar clouds. This suggests the building blocks of life may be widespread across the universe.',
   'What does the presence of organic molecules in space suggest about life elsewhere?',
   'Space Chemistry'),

_d('ff014','funfact','🦾','Your Body Replaces Most of Its Cells Every 7–10 Years',
   'You are quite literally not the same person you were a decade ago.',
   'Different cells replace themselves at different rates: skin cells every 2–3 weeks, red blood cells every 4 months, gut cells every 2–5 days. Liver cells take about a year. Heart muscle cells replace very slowly — only about 1% per year. Some brain neurons last your entire lifetime. So you are a constantly renewing system — though your DNA stays the same throughout.',
   'Which parts of your body are "oldest"? Research which cells do NOT replace themselves.',
   'Biology'),

_d('ff015','funfact','🌪️','A Bolt of Lightning Is Five Times Hotter Than the Surface of the Sun',
   'Lightning reaches about 30,000 Kelvin — the Sun\'s surface is only about 5,800 Kelvin.',
   'A lightning bolt is an electrical discharge caused by charge separation inside a storm cloud. When it strikes, the channel heats almost instantaneously to around 30,000 K — five times the Sun\'s surface temperature. This extreme heating causes the surrounding air to expand rapidly, creating the shockwave we hear as thunder. Sound travels at 343 m/s — you can calculate how far away a strike is.',
   'If lightning is hotter than the Sun, why does the Sun feel hotter to us?',
   'Physics'),

_d('ff016','funfact','🍌','Bananas Are Berries — Strawberries Are Not',
   'Botanically, a banana qualifies as a berry, but a strawberry does not.',
   'In botany, a **berry** is a fruit that develops from one flower with one ovary and has seeds embedded in the flesh. Bananas fit this definition. Strawberries develop from multiple ovaries and have seeds on the outside, so they are called **aggregate fruits**. Watermelons, cucumbers, and pumpkins also count as berries by the scientific definition.',
   'Name three other foods that are technically berries.'),

_d('ff017','funfact','💩','Wombat Poop Is Cube-Shaped',
   'Wombats are the only animals known to produce cube-shaped droppings.',
   'Scientists discovered that wombat intestines have irregular muscle contractions that shape poop into cubes. This unique shape prevents the droppings from rolling away, helping wombats mark their territory on rocks and logs. Each wombat produces up to 100 cubes per day. Researchers have studied this to understand soft-tissue engineering and even manufacturing cube-shaped objects.',
   'Why might cube-shaped poop be useful for marking territory?'),

_d('ff018','funfact','🌞','A Day on Mercury Lasts Longer Than Its Year',
   'Mercury spins so slowly that it completes an orbit around the Sun before one full rotation.',
   'Mercury takes 88 Earth days to orbit the Sun — that is its year. But it takes 176 Earth days to rotate once — that is its day. So a day on Mercury is about twice as long as its year! Because it has almost no atmosphere, temperatures swing wildly: 430°C during the day and -180°C at night.',
   'Would you rather have very long days or very long nights?'),

_d('ff019','funfact','🐄','Cows Have Best Friends',
   'Cows form close social bonds with other cows and get stressed when separated.',
   'Research from the University of Northampton found that cows have preferred companions. When kept with their best friend, they show lower heart rates and less stress. Cows are also highly social animals with complex herd dynamics. Farmers who understand this can improve animal welfare by keeping friends together.',
   'What animal friendships have you observed?'),

_d('ff020','funfact','👃','You Cannot Hum While Holding Your Nose',
   'Try it — humming requires air to move through your nose.',
   'When you hum, your vocal cords vibrate and create sound, but the sound escapes through your nose. If you pinch your nose shut, the airflow is blocked and the humming stops. This is a simple party trick that demonstrates how sound needs a pathway to travel. It also shows how connected your mouth, throat, and nose are for making sound.',
   'Test this on a friend. Can they figure out why it works before you explain?'),
]

# ── 2-MINUTE HACKS ────────────────────────────────────────────────────────────
HACKS = [
_d('hk001','hack','⏱️','The 2-Minute Rule for Beating Procrastination',
   'If a task takes less than 2 minutes — do it immediately. No exceptions.',
   'Popularized by productivity expert David Allen, the **2-Minute Rule** cuts through decision fatigue. Every small task you defer creates mental load — it sits in your head taking up space. Replying to that message, putting that thing away, writing that reminder — if it takes under 2 minutes, stopping to do it immediately is faster than remembering to do it later. Try it for one day and notice the difference.',
   'Identify every task you\'ve been deferring that would take under 2 minutes. Do them now.',
   'Productivity'),

_d('hk002','hack','📚','The "5-4-3-2-1" Method to Start Studying',
   'Count backwards from 5 and move your body before your brain can argue.',
   'Created by Mel Robbins: when you need to start something hard, count 5-4-3-2-1 then physically move. No thinking — just move. This interrupts the hesitation loop in your brain. The key is the physical movement — stand up, open the book, put the first word on the page. Once you start, friction disappears. Most "hard" tasks are only hard to begin.',
   'Try it right now for something you\'ve been avoiding. 5-4-3-2-1. Move.',
   'Psychology'),

_d('hk003','hack','💤','Box Breathing to Calm Down in 2 Minutes',
   'Used by Navy SEALs before high-stress situations — it works for anyone.',
   '**Box breathing**: Inhale for 4 counts → Hold for 4 counts → Exhale for 4 counts → Hold for 4 counts → Repeat 4 times. This activates your parasympathetic nervous system — the "rest and digest" mode — and lowers heart rate within 90 seconds. It reduces cortisol (stress hormone) and improves focus. Use it before a test, a difficult conversation, or when overwhelmed.',
   'Practice box breathing right now. Notice what changes in your body after 2 minutes.',
   'Mental Health'),

_d('hk004','hack','🧠','The Feynman Technique for Learning Anything',
   'If you can\'t explain it simply, you don\'t understand it yet.',
   'Named after Nobel Prize physicist Richard Feynman: **1.** Pick a concept. **2.** Explain it out loud as if teaching a 10-year-old. **3.** Notice where you stumble or get vague — those are the gaps. **4.** Go back and fill the gaps. **5.** Simplify again. This forces real understanding, not just memorization. It is the most effective study method research has confirmed.',
   'Pick one thing you "know" and try to explain it out loud to nobody. Find your gaps.',
   'Study Hack'),

_d('hk005','hack','💧','Drink Water First Thing in the Morning',
   'Your brain is 75% water — and you just went 8 hours without drinking any.',
   'While you sleep you lose water through breathing and sweating. Mild dehydration — even 1–2% — reduces concentration, memory, and mood. Drinking 250–500ml of water within 10 minutes of waking rehydrates your brain, kickstarts your metabolism, and flushes overnight waste products. Add a squeeze of lemon for vitamin C. Coffee dehydrates slightly — water first, coffee second.',
   'Keep a glass of water beside your bed tonight. Drink it the moment you wake.',
   'Health'),

_d('hk006','hack','📝','Write Tomorrow\'s Top 3 Tasks Tonight',
   'A 2-minute evening habit that eliminates morning decision paralysis.',
   'Before bed, write exactly three things that MUST happen tomorrow — not ten, not five. Three. This clears mental chatter so your brain can rest (less unfinished-task rumination during sleep). Morning decision-making is worst because willpower is highest but context is lowest. Your written 3 tasks create instant clarity — you wake up knowing exactly what to do first.',
   'Write your top 3 for tomorrow right now. Put the list somewhere you will see it at breakfast.',
   'Productivity'),

_d('hk007','hack','🎧','Use Background Noise at 70 dB for Deep Focus',
   'Complete silence and loud music both hurt focus. Medium noise (coffee shop level) helps.',
   'Research from the Journal of Consumer Research found that **ambient noise at 70 decibels** — roughly the volume of a coffee shop or light rain — optimally boosts creative and cognitive performance. Complete silence reduces distraction but can feel oppressive for many people. Loud music (above 85 dB) disrupts linguistic processing. Try a "brown noise" or lo-fi playlist next time you study.',
   'Study with ambient coffee shop noise for one session. Compare your focus level.',
   'Study Hack'),

_d('hk008','hack','📱','The "App Graveyard" Folder Hack',
   'Move every app you mindlessly open to a folder on the last screen. Use friction to break habits.',
   'You open Instagram or YouTube on autopilot — the app is at your fingertips, the habit fires instantly. Friction reduces habits: move those apps into a folder named "Apps I Need To Decide About" on the last screen of your phone. Now opening them requires 3 extra taps and a deliberate choice. Studies show this reduces mindless usage by 20–30%. It is not blocking — it is making the habit conscious.',
   'Reorganize your phone: move your top 3 time-sink apps to the last screen. Track time today vs. tomorrow.',
   'Digital Wellness'),

_d('hk009','hack','🏃','The 10-Minute Walk Rule for Creativity',
   'Stuck on a problem? Walk away — literally. Your brain keeps working.',
   'Stanford research showed that walking increases creative output by 81%. When you hit a wall on a problem, walking activates the **default mode network** — the part of your brain that works in the background connecting ideas. The walk does not have to be outside. Even a treadmill works. Come back to the problem after 10 minutes and notice what surfaced.',
   'Next time you are stuck on homework, set a 10-minute walk timer. Do not think about the problem on purpose.',
   'Science of Thinking'),

_d('hk010','hack','🔡','Chunking to Remember Long Numbers',
   'Your working memory holds 7 ± 2 items — but chunks count as one item each.',
   '**Chunking** means grouping individual items into meaningful groups. A phone number: 9876543210 is 10 separate digits — hard to hold. 98-765-432-10 is 4 chunks — manageable. Credit cards are displayed in groups of 4 for this reason. You can chunk by sound (words), meaning (familiar patterns), or visual pattern. This is how experts "remember" far more than novices — they chunk at a higher level.',
   'Memorize your emergency contact\'s phone number using chunking. Test yourself tomorrow.',
   'Memory Science'),

_d('hk011','hack','🌿','The 20-20-20 Rule for Eye Strain',
   'Every 20 minutes, look at something 20 feet away for 20 seconds.',
   'Digital eye strain (also called computer vision syndrome) affects over 60% of screen users. The ciliary muscles in your eye contract when focusing on close screens — held position for too long causes fatigue, headaches, and blurred vision. The **20-20-20 rule** relaxes these muscles by refocusing on a distant object. Set a timer. It takes 20 seconds and dramatically reduces strain over a day.',
   'Set a 20-minute timer right now. Every ring, look out a window for 20 seconds.',
   'Health'),

_d('hk012','hack','🎯','Temptation Bundling for Hard Tasks',
   'Pair something you love with something you avoid. Only allow the thing you love during the avoided task.',
   'Behavioural economist Katherine Milkman\'s research: pair a guilty pleasure with an unpleasant task. Examples: only listen to your favourite podcast while doing chores. Only watch a specific show while exercising. Only have a favourite drink while doing homework. This creates positive anticipation for the dreaded task and associates it with pleasure over time. It rewires habit loops.',
   'Design your own temptation bundle for your least favourite task this week.',
   'Psychology'),

_d('hk013','hack','📖','Read 10 Pages a Day to Finish 12+ Books a Year',
   '10 pages takes 15–20 minutes. At this pace you read a book a month without trying.',
   'The average book is 250–300 pages. At 10 pages per day — 15–20 minutes reading — you finish a book in 25–30 days, or roughly 12–15 books per year. Most successful people in the world are voracious readers: Warren Buffett reads 500 pages per day; Bill Gates reads 50 books per year. Reading improves vocabulary, empathy, and intelligence measurably. Start with 10 pages before bed.',
   'Pick a book today. Read the first 10 pages tonight. Set a recurring reminder.',
   'Life Upgrade'),

_d('hk014','hack','🛏️','Make Your Bed in Under 2 Minutes',
   'Research links making your bed to higher productivity, better sleep, and greater willpower.',
   'Admiral William McRaven\'s 2014 commencement speech made this famous: "If you make your bed every morning you will have accomplished the first task of the day." Research from the National Sleep Foundation found that people who make their beds are 19% more likely to sleep better. It takes 90–120 seconds. The act creates a physical anchor for a productive morning routine.',
   'Make your bed for 30 days straight. Track whether it affects your mornings.',
   'Morning Win'),

_d('hk015','hack','🔋','Charge Your Brain With a 20-Minute Nap',
   'NASA research: a 26-minute nap improved pilot performance by 34% and alertness by 100%.',
   'A short nap (10–20 minutes) reaches Stage 2 sleep — restoring alertness and motor performance without grogginess. Longer naps (30+ minutes) enter deeper sleep and cause "sleep inertia" — that heavy, confused feeling when you wake. The optimal nap: 20 minutes, ideally 6–8 hours after waking. Some researchers suggest a "nappuccino" — drink coffee, nap 20 min, wake up as caffeine kicks in.',
   'Try a 20-minute nap today. Set an alarm. Note how you feel after.',
   'Performance'),

_d('hk016','hack','🍅','The Pomodoro Technique for Homework',
   'Study for 25 minutes, rest for 5. Repeat. Your brain stays fresh longer.',
   'Named after a tomato-shaped kitchen timer, the **Pomodoro Technique** breaks work into focused 25-minute chunks followed by short breaks. After four rounds, take a longer 15–30 minute break. This works because your brain\'s attention naturally dips after 20–30 minutes. Short breaks restore focus and prevent burnout better than one long slog.',
   'Try one Pomodoro session on your next homework assignment.'),

_d('hk017','hack','🎒','Pack Your Bag the Night Before',
   'A 5-minute evening habit prevents morning panic.',
   'Morning willpower is low and time is short. Packing your bag the night before removes a decision from your morning and prevents forgotten homework, lunch boxes, or gym clothes. Lay out your clothes too if possible. These small evening habits create calmer mornings and fewer family arguments.',
   'Pack tonight\'s bag right now and list three things you would have forgotten.'),

_d('hk018','hack','🧠','Use Mnemonics to Remember Lists',
   'Turn boring lists into funny sentences and they stick in your memory.',
   'A **mnemonic** is a memory trick. To remember the planets in order: **M**y **V**ery **E**ager **M**other **J**ust **S**erved **U**s **N**achos (Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune). The sillier the sentence, the better it sticks. You can create mnemonics for spelling, math rules, history dates, or any list.',
   'Create a mnemonic to remember the first 8 U.S. presidents or your locker combination.'),

_d('hk019','hack','🐸','Eat the Frog First',
   'Do your hardest task first thing — everything else feels easier after.',
   'The phrase "eat the frog" comes from a Mark Twain quote: if you eat a live frog first thing, nothing worse will happen all day. Applied to work, it means tackle your most important or dreaded task before anything else. Willpower is highest in the morning, and completing the hard thing creates momentum for the rest of the day.',
   'What is your "frog" tomorrow? Do it before checking your phone.'),

_d('hk020','hack','🤸','Stretch Between Study Sessions',
   'Two minutes of movement resets your brain better than scrolling.',
   'Sitting still for long periods reduces blood flow to the brain and makes you sleepy. Every 30–45 minutes, stand up, touch your toes, roll your shoulders, or do five jumping jacks. Movement increases oxygen to the brain, improves mood, and helps you retain information better than pushing through fatigue.',
   'Set a timer and stretch for 2 minutes between every study block today.'),
]

# ── GAMES ─────────────────────────────────────────────────────────────────────
GAMES = [
_d('gm001','game','🎮','20 Questions — The Classic Thinking Game',
   'One person thinks of something. Others get 20 yes/no questions to figure it out.',
   '**How to play:** One player thinks of any object, person, animal, or concept. Other players take turns asking yes/no questions. Classic openers: "Is it alive?" → "Is it bigger than a car?" → "Is it found in a kitchen?" The goal is to narrow the category systematically — broad first, specific later. The thinker can only answer Yes, No, or Sometimes. Solved in 20 questions or fewer? Questioners win.',
   'Play 20 Questions with a friend or family member. Try to solve it in fewer than 15 questions.',
   '2+ Players'),

_d('gm002','game','✏️','The Exquisite Corpse Drawing Game',
   'Each person draws a section of a creature without seeing what the others drew.',
   '**How to play:** Fold a paper into thirds. Person 1 draws a head, folds it over to hide it, leaving only the neck lines visible. Person 2 draws a body, folds it. Person 3 draws legs. Unfold to reveal the absurd creature. Invented by Surrealist artists in the 1920s — they used it to unlock unconscious creativity. You can play with words too: subject — verb — object, each hidden before passing.',
   'Play Exquisite Corpse with 3+ people today. Share the results.',
   '3+ Players'),

_d('gm003','game','🧮','21 — The Mental Math Card Game',
   'Get as close to 21 as possible without going over. Pure probability and strategy.',
   '**How to play (simplified):** Use a standard deck. Each player is dealt 2 cards. Face cards = 10, Aces = 1 or 11, others = face value. Players choose to "hit" (take a card) or "stand." Go over 21 = bust. Highest score under 22 wins. This is the basis of Blackjack. The skill: estimating probability based on cards already seen (card counting is a real mathematical technique).',
   'Play 21 with a friend. Try to track which high cards have already appeared.',
   '2+ Players'),

_d('gm004','game','📝','Codenames — The Word Association Team Game',
   'Two teams race to identify secret codenames using one-word clues.',
   '**How to play:** 25 word cards are laid in a 5×5 grid. Each team has a Spymaster who knows which words belong to their team. The Spymaster gives a one-word clue + a number ("Animals: 3") and teammates try to identify the 3 words connected by that clue. Touch the wrong card — give points to the other team. Touch the Assassin — instant loss. Requires creative lateral thinking.',
   'Play Codenames online free at codenames.game — you can play without any equipment.',
   'Team Game'),

_d('gm005','game','🎯','Dots and Boxes — The Classic Pencil Strategy Game',
   'Draw lines to claim boxes. The player who completes the most boxes wins.',
   '**How to play:** Draw a grid of dots (start with 5×5). Players take turns drawing one horizontal or vertical line between adjacent dots. When you complete the fourth side of a box, write your initial inside and take another turn. Strategy: avoid completing the third side of boxes — you are setting up your opponent. Advanced play involves sacrifice chains — giving away boxes to gain larger ones.',
   'Play on paper with a friend using a 6×6 dot grid. Find the optimal strategy.',
   '2 Players'),

_d('gm006','game','🧩','SET — The Real-Time Pattern Recognition Game',
   'Find sets of 3 cards where each attribute is either all the same or all different.',
   '**How to play:** Cards have 4 attributes — number (1/2/3), shape (oval/diamond/squiggle), shading (solid/striped/open), and color (red/green/purple). A valid SET: all 3 cards are either all the same or all different in EVERY attribute. 12 cards are laid face-up. First to call and correctly identify a SET takes the cards. Studies show SET improves visual processing speed and pattern recognition.',
   'Download the free SET Daily Puzzle online and try to beat the timer.',
   'Brain Training'),

_d('gm007','game','📖','Story Dice — Collaborative Storytelling',
   'Roll dice with pictures. Build a story using everything that comes up.',
   '**How to play:** Use Rory\'s Story Cubes (or draw 9 symbols on paper pieces). Roll all dice. One player starts a story using the first symbol. Each next player adds a sentence using the next symbol. The story must stay coherent — but creativity is rewarded. Constraints force creativity: the limitation of "you MUST use this image" triggers lateral thinking that total freedom often does not.',
   'Draw 6 random symbols. Set a timer for 3 minutes. Tell a complete story using all 6.',
   '1+ Players'),

_d('gm008','game','🔤','Ghost — The Word Game That Never Ends Badly',
   'Add a letter to a growing string without completing a real word. Whoever finishes a word loses.',
   '**How to play:** Players take turns adding one letter to a string. You must have a real word in mind (you cannot bluff with random letters). But do NOT complete a real word — the player who makes a complete word loses that round. Strategy: plan ahead, steer toward long words (longer = more letters before completion). If challenged on your letter choice, you must reveal your word or lose.',
   'Play Ghost with 3 people. Try to steer toward 8+ letter words.',
   '2+ Players'),

_d('gm009','game','🎭','Reverse Charades — Act for Your Team, Not Against Them',
   'Instead of one person acting for the group, the whole group acts for one person to guess.',
   '**How to play:** One person faces away from the group (the guesser). A card shows a word or phrase. The entire rest of the group acts it out simultaneously — no speaking, no pointing at objects in the room. The guesser calls out answers. In a time limit (60 seconds), guess as many as possible. The team dynamic — everyone acting together — creates hilarious chaos and high success rates.',
   'Play with at least 4 people. Use movie titles as the prompts.',
   '4+ Players'),

_d('gm010','game','♟️','Mini Chess — Learn Endgame in 15 Minutes',
   'Play on a 5×5 board with 5 pieces. Learn chess strategy without the complexity.',
   '**How to play (Gardner Mini Chess):** Use a 5×5 board. Each side has: King, Queen, Rook, Bishop, Knight — one of each, on the back row. Standard chess rules apply. The reduced board forces immediate strategic thinking — there is no slow opening game. Mini chess is used in schools worldwide to teach chess principles quickly. Once you can play 5×5 well, moving to the full board feels natural.',
   'Set up a 5×5 chess board and play 3 games. Focus on controlling the center.',
   '2 Players'),

_d('gm011','game','🔢','24 — The Mental Arithmetic Challenge',
   'Use any four numbers and basic operations (+−×÷) to make exactly 24.',
   '**How to play:** Draw 4 cards from a deck (face cards = 10). Use each card exactly once. Use any combination of addition, subtraction, multiplication, or division. You must reach exactly 24. Example: 3, 8, 3, 8 → 8 ÷ (3 − 8/3) = 24. Some combinations have only one solution; some have many; a few have none. Trains flexible arithmetic thinking faster than most math homework.',
   'Try these four sets: [1, 2, 3, 4] then [3, 3, 8, 8] then [1, 5, 5, 5]. Find 24 each time.',
   'Math Game'),

_d('gm012','game','🌍','Geoguessr — Guess Where in the World You Are',
   'You are dropped randomly on Google Street View. Clues in the environment tell you your location.',
   'GeoGuessr drops you somewhere in the world via Google Street View. No labels. You look at vegetation, road signs, car types, architecture, road markings, and landscape to deduce the country, then region, then city. Professional players can identify a country from a single blurry screenshot in under a second. It builds real geographic literacy, pattern recognition, and cultural awareness.',
   'Play 5 rounds of the free daily GeoGuessr challenge. Track which clues help most.',
   'Solo / Team'),

_d('gm013','game','🃏','Spit — The Fastest Card Game You Will Ever Play',
   'Both players flip cards simultaneously into shared piles. First to empty their deck wins.',
   '**How to play:** Two players each get half a deck. Set up 5 stockpiles each. Flip simultaneously into two central piles — play any card within ±1 of a central pile\'s top card (7 on 6 or 8; any card on Ace). Keep both hands moving. No turns — pure simultaneous speed. Shout "Spit!" to add a fresh card to each central pile when stuck. First player to empty all stockpiles wins.',
   'Learn Spit and play 5 rounds. Your speed will improve dramatically by round 3.',
   '2 Players'),

_d('gm014','game','🧠','Dual N-Back — Train Your Working Memory',
   'The only brain training game with strong scientific evidence for improving fluid intelligence.',
   '**How to play:** Two streams of information are presented simultaneously — a visual position (grid square) and an audio letter. Your job: press a key when either stimulus matches what appeared N steps back. Start at N=2 (2 steps back). As you improve, increase to 3, 4. Studies (including a meta-analysis of 40 trials) show sustained Dual N-Back training measurably improves working memory and fluid IQ. Free versions exist online.',
   'Play Dual N-Back for 20 minutes daily for two weeks. Track your N-level improvement.',
   'Solo Brain Training'),

_d('gm015','game','🎲','Pandemic — The Cooperative Strategy Game',
   'You are a team of disease-fighting specialists. Save the world — or lose together.',
   '**How to play:** 2–4 players each have unique roles (Medic, Scientist, Dispatcher). Four diseases are spreading across the world map. On each turn: take 4 actions (move, treat, build, share knowledge), draw 2 player cards, then spread disease. If any disease spreads too fast — game over. Pandemic requires communication, role optimization, and strategic prioritization. It teaches systems thinking.',
   'Play Pandemic with family or friends. Debrief: what strategy worked? What did not?',
   '2–4 Players'),

_d('gm016','game','👂','Simon Says — The Classic Listening Game',
   'A simple game that trains attention, impulse control, and listening skills.',
   '**How to play:** One player is Simon and gives commands like "Simon says touch your nose." Players must only follow commands that begin with "Simon says." If Simon gives a command without saying "Simon says" first, anyone who follows it is out. The last player standing becomes the next Simon. It is surprisingly hard — your brain wants to react automatically.',
   'Play three rounds of Simon Says. Notice how hard it is to stop yourself.'),

_d('gm017','game','👁️','I Spy — Observation on the Go',
   'A no-equipment game perfect for car rides, waiting rooms, or classrooms.',
   '**How to play:** One player picks an object they can see and says, "I spy with my little eye something that is..." followed by a color, shape, or first letter. Other players take turns guessing until someone identifies the object. It sharpens observation skills and vocabulary, and works anywhere you can look around.',
   'Play I Spy during your next car ride or meal wait.'),

_d('gm018','game','⬜','Hopscotch — Math and Movement Combined',
   'Draw a grid, toss a stone, and hop your way through numbers.',
   '**How to play:** Draw a hopscotch grid with numbered squares. Toss a small object onto a square. Hop through the grid, skipping the square with the object, then turn around and come back. You can make it harder by adding math problems: solve 7 + 5 before landing on square 12. It builds balance, coordination, and number sense at the same time.',
   'Design your own hopscotch grid with a twist — math problems or spelling words.'),

_d('gm019','game','🔤','Hangman — Word Guessing Classic',
   'Guess the hidden word one letter at a time before the drawing is complete.',
   '**How to play:** One player thinks of a word and draws blanks for each letter. Others guess letters one at a time. Correct letters are filled in; incorrect letters add parts to a stick-figure drawing. Guess the word before the drawing is finished. Strategy: start with common vowels (E, A, O) and consonants (T, S, R, N). Great for spelling and vocabulary practice.',
   'Play Hangman with a friend using words from this week\'s spelling list.'),

_d('gm020','game','🎵','Musical Chairs — Quick Reflexes and Laughter',
   'Walk, music stops, grab a chair. One chair fewer than players.',
   '**How to play:** Arrange chairs in a circle, one fewer than the number of players. Players walk around the chairs while music plays. When the music stops, everyone must sit. The player left standing is out. Remove one chair and repeat until one winner remains. It is simple, fast, and guaranteed to produce laughter. Make it educational by answering a trivia question to stay in.',
   'Organize a Musical Chairs game with friends or family this week.'),
]

# ── TRENDING KIDS STUFF ────────────────────────────────────────────────────────
TRENDING = [
_d('tr001','trending','🤖','AI Art: How Machines Learned to Draw',
   'AI image generators like Midjourney and DALL-E can create stunning art from text prompts.',
   'In 2022, AI image generation went mainstream. Tools like Midjourney, DALL-E, and Stable Diffusion can turn any text description into a detailed image in seconds. They were trained on hundreds of millions of images from the internet. Artists are debating whether AI art is "real" creativity, and schools are updating policies on AI-generated content. Some students are learning **prompt engineering** — the skill of writing descriptions that produce great AI art.',
   'Try a free AI image generator with a creative prompt. What surprised you about the result?',
   'Tech Trend'),

_d('tr002','trending','🌱','Gen Z Is Changing How the World Eats',
   'Younger generations are driving the biggest shift in food habits in decades.',
   'Gen Z eats significantly less meat than previous generations — studies show 65% have reduced meat consumption. Plant-based foods (Beyond Meat, oat milk, tofu bowls) are growing fastest among under-25s. There is also a rise in "food as identity" — sharing meals on TikTok, caring about where food comes from, and challenging fast food culture. Food companies are racing to adapt their menus.',
   'Audit your meals this week. What percentage is plant-based? Could you try one new plant-based food?',
   'Food & Planet'),

_d('tr003','trending','🎵','How Bedroom Producers Are Taking Over Music',
   'Some of the world\'s biggest hits are made by teenagers in their bedrooms.',
   'Billie Eilish recorded her first major album "When We All Fall Asleep" in her brother Finneas\'s bedroom. Music production software like GarageBand, FL Studio, and Ableton has become affordable or free. YouTube and TikTok let artists reach millions without a record label. Today, more music is released independently than through major labels. The bedroom producer era has democratized one of the world\'s biggest industries.',
   'Look up how your favourite song was recorded. Was any part made at home?',
   'Music Industry'),

_d('tr004','trending','🧬','CRISPR: The Gene-Editing Tool That Could Change Medicine',
   'Scientists can now edit DNA the way you edit text — precisely and cheaply.',
   'CRISPR-Cas9, discovered as a natural bacterial immune system, is now used to edit genes. In 2023, the first CRISPR-based treatment for sickle cell disease was approved. Doctors edited patients\' own bone marrow cells, and most became symptom-free. In the future, CRISPR could treat cancer, blindness, and genetic disorders. Ethical debates are ongoing about using it to edit embryos.',
   'Research one disease that CRISPR might cure. What are the ethical concerns?',
   'Biotech'),

_d('tr005','trending','🏙️','Minecraft Generations: Why It Never Gets Old',
   'Minecraft has sold over 300 million copies — it is the best-selling video game of all time.',
   'Released in 2011, Minecraft still grows every year. Its secret: it is a creativity engine, not a game with an endpoint. Players build, explore, program (with Redstone circuits), and even learn computer science. Schools worldwide use Minecraft Education Edition for history, architecture, and coding lessons. The game\'s "sandbox" design — total freedom — is now the model for a genre of games.',
   'Build something in Minecraft that has educational value — a historical monument, a working calculator, or a lesson environment.',
   'Gaming Culture'),

_d('tr006','trending','📱','Why Everyone Is Talking About Digital Minimalism',
   'A growing movement of young people is choosing to use less technology — intentionally.',
   'Digital minimalism is the practice of deliberately reducing screen time to use technology only for things that truly add value. Books like Cal Newport\'s "Digital Minimalism" and "Deep Work" have driven the trend. Some teens are switching back to dumb phones or flip phones. Research links heavy social media use to increased anxiety — the movement is a response to the attention economy designed to maximize screen time.',
   'Track your screen time today. Which apps give you value? Which ones just consume time?',
   'Digital Wellness'),

_d('tr007','trending','🎒','The Rise of Study TikTok and "StudyTube"',
   'Millions of students study alongside strangers on YouTube and TikTok live streams.',
   '"Study with me" videos — someone studying silently on camera — have billions of views. "Studygramers" and "StudyTubers" share revision notes, stationery hauls, and real-time study sessions. The trend works because of **body doubling** — a psychology phenomenon where having another person present (even virtually) improves focus, especially for people with ADHD. Accountability and ambient human presence help.',
   'Try a "study with me" YouTube stream for your next study session. Does it help your focus?',
   'Study Culture'),

_d('tr008','trending','🌊','Ocean Cleanup: Gen Z\'s Answer to Plastic Pollution',
   'A Dutch inventor who pitched his idea at age 18 is cleaning the Great Pacific Garbage Patch.',
   'Boyan Slat was 16 when he had the idea for The Ocean Cleanup project. At 18, he published his first research paper. By his twenties he had raised millions and launched the world\'s largest ocean cleanup systems. His U-shaped barriers catch plastic using natural ocean currents — no nets that could trap sea life. The project has removed over 10 million kilograms of plastic so far.',
   'What plastic items do you use most? Which could you replace with something reusable?',
   'Environment'),

_d('tr009','trending','🧠','Why "Quiet Quitting" and "Soft Life" Are Trending',
   'Young people are pushing back against hustle culture — and the data says why.',
   '"Quiet quitting" means doing only what your job requires — no more. "Soft life" means deliberately choosing comfort, rest, and joy over achievement at all costs. These trends reflect burnout among young people and a rejection of the "hustle 24/7" mindset. Studies show overwork reduces productivity after 50 hours per week. Working smarter — not longer — is the science-backed alternative.',
   'Design your ideal work-life balance. How many hours per day would go to each activity?',
   'Lifestyle Shift'),

_d('tr010','trending','🏋️','Why Strength Training Is Exploding Among Teens',
   'More young people are picking up weights — and the research strongly supports it.',
   'Strength training among teenagers is at an all-time high, driven partly by fitness content on TikTok and YouTube. Research shows resistance training improves bone density, posture, mental health, and academic performance. Contrary to old myths, strength training does NOT stunt growth in young people when done properly. Bodyweight exercises — push-ups, squats, lunges — require zero equipment and are clinically proven effective.',
   'Try a 7-minute bodyweight workout today. Just push-ups, squats, and a plank. No equipment.',
   'Health Trend'),

_d('tr011','trending','🎨','Why Cottagecore and Dark Academia Are More Than Aesthetics',
   'Visual "aesthetics" on social media are actually shaping how millions of teens see the world.',
   'Aesthetics like **Cottagecore** (nature, simplicity, baking bread), **Dark Academia** (classical literature, Gothic architecture, autumn libraries), and **Solarpunk** (renewable tech meets nature) are more than visual styles. They reflect values — anti-consumerism, connection to history, optimism about the future. Social media created a new type of cultural identity: curated visual worldviews shared across continents.',
   'Define your own "aesthetic" in 5 words. What values does it reflect?',
   'Culture & Identity'),

_d('tr012','trending','🚗','The Electric Vehicle Revolution: Faster Than Anyone Expected',
   'In 2023, 1 in 5 cars sold in China was electric. The world is changing faster than predicted.',
   'Electric vehicles (EVs) went from novelty to mainstream in less than a decade. Tesla, BYD (China), and dozens of traditional automakers are competing for the EV market. Charging networks are expanding rapidly. Range anxiety — fear of running out of battery — is declining as average EV range exceeds 400 km. By 2035, many countries will ban new petrol car sales.',
   'Research: what percentage of cars in your country are electric? What is the target for 2030?',
   'Tech & Environment'),

_d('tr013','trending','🧶','The Craft Comeback: Why Young People Are Knitting and Making Again',
   'Craft hobbies — knitting, ceramics, woodworking, journaling — are surging among teens.',
   'Sales of craft supplies hit record highs during and after the pandemic. Knitting, embroidery, pottery, and even blacksmithing are trending on social media. Why? Making physical objects provides the **completion loop** that digital work often lacks — a visible, tangible result. Craft also reduces anxiety: repetitive physical motion activates the parasympathetic nervous system. It is analog self-care.',
   'Try making one physical object this week — draw, build, sew, cook, or write by hand.',
   'Creativity Trend'),

_d('tr014','trending','🌐','The Metaverse: What Happened to the Hype?',
   'Meta spent $36 billion building a virtual world. Almost nobody showed up. What went wrong?',
   'In 2021, Facebook rebranded to Meta and declared the future was the **metaverse** — immersive virtual worlds for work and play. By 2023, their VR world Horizon Worlds had fewer than 200,000 active users. Critics pointed to uncomfortable headsets, poor graphics, a lack of compelling use cases, and underestimating how much people prefer real human interaction. The hype collapsed — but VR technology continues to improve in specific use cases like training, therapy, and gaming.',
   'What would a truly compelling virtual world need to offer to get you to use it daily?',
   'Tech Reality Check'),

_d('tr015','trending','📊','Why Data Literacy Is the New Literacy',
   'In a world drowning in statistics, knowing how to read a graph correctly is a superpower.',
   'Every day we are shown statistics — infection rates, economic data, sports analytics, climate figures. Data literacy means understanding what a graph is actually showing, what it is NOT showing, and when numbers are being used to mislead. Common tricks: cut y-axes that exaggerate changes, percentages without base numbers, correlation presented as causation. Being data-literate makes you almost immune to manipulation.',
   'Find a graph in today\'s news. Ask: what does this NOT show? Who benefits from this framing?',
   'Critical Skill'),

_d('tr016','trending','🏓','Pickleball Is Taking Over the World',
   'A paddle sport that is easy to learn, social, and fun for all ages.',
   'Pickleball combines elements of tennis, badminton, and ping-pong. It is played on a smaller court with a plastic ball and paddles. It has become the fastest-growing sport in many countries because it is low-impact, inexpensive, and easy for beginners. Schools, parks, and retirement communities now share courts. Professional leagues and celebrity investors are making it a serious sport too.',
   'Try pickleball if you can. What skills from other sports help you play?'),

_d('tr017','trending','💧','Reusable Water Bottles Are a Status Symbol',
   'A simple swap became a lifestyle statement — and it helps the planet.',
   'Brands like Stanley, Hydro Flask, and Nalgene turned reusable bottles into must-have accessories. Carrying a refillable bottle reduces single-use plastic waste and saves money. Some schools and airports now have water-bottle refill stations. The trend shows how small sustainable choices can become cool cultural symbols.',
   'Calculate how many plastic bottles you would save in a year by using a reusable one daily.'),

_d('tr018','trending','🌿','Plant Parenting Is the New Pet',
   'Young people are growing indoor gardens and sharing them online.',
   'Caring for houseplants has become hugely popular. Plants like pothos, succulents, and snake plants are beginner-friendly and improve indoor air quality. "Plant parents" track growth, name their plants, and troubleshoot problems on social media. Gardening reduces stress and teaches responsibility — even a single windowsill plant counts.',
   'Start with one easy indoor plant. Research how much light and water it needs.'),

_d('tr019','trending','📱','Short Educational Videos Are Changing Learning',
   'TikTok, YouTube Shorts, and Instagram Reels now teach science, history, and languages.',
   'Educational creators use short videos to explain complex topics in 60 seconds or less. This format makes learning feel fun and accessible. However, short videos can oversimplify. The best learners use them as a starting point and then dive deeper with books, articles, or courses. Critical thinking still matters in snack-sized content.',
   'Find one educational short video today and fact-check one claim from it.'),

_d('tr020','trending','👕','Upcycling Fashion Is Trending',
   'Young designers turn old clothes into new styles instead of buying fast fashion.',
   'Upcycling means transforming old or discarded items into something better. In fashion, this means cutting, dyeing, sewing, or patching old clothes into unique outfits. It fights textile waste — the fashion industry produces over 90 million tons of waste yearly. Thrifting and upcycling are now seen as creative and environmentally responsible style choices.',
   'Design an outfit using only clothes you already own.'),
]

# ── NEWS ──────────────────────────────────────────────────────────────────────
NEWS = [
_d('nw001','news','🧬','Scientists Grow Replacement Skin in a Lab',
   'Researchers have created lab-grown skin with hair follicles — a first for burn victims.',
   '**What happened:** Scientists at a research hospital successfully grew human skin in a laboratory that contains working hair follicles, sweat glands, and blood vessels. This is a significant leap forward from earlier lab-grown skin, which was flat and featureless.\n\n**Why it matters:** Millions of people worldwide suffer from severe burns each year. Until now, skin grafts required taking skin from another part of the patient\'s body, which is painful and leaves scars. Lab-grown skin could eliminate that second surgery entirely.\n\n**What\'s next:** The team expects clinical trials on burn patients to begin within three years. If approved, it could change treatment for burn victims, people with skin diseases like epidermolysis bullosa, and even cosmetic surgery.',
   'Research the difference between a skin graft and lab-grown skin. Which sounds more comfortable?',
   'Science'),

_d('nw002','news','🐋','Humpback Whales Are Making a Remarkable Comeback',
   'Once hunted nearly to extinction, humpback whale populations have recovered dramatically.',
   '**What happened:** New population surveys published by marine biologists confirm that humpback whale numbers in the South Atlantic have recovered to approximately 25,000 — up from fewer than 450 in the 1950s after decades of commercial whaling.\n\n**Why it matters:** This is one of conservation\'s great success stories. After the International Whaling Commission banned commercial whaling in 1986, populations began recovering. It proves that when humans stop a harmful activity, nature can heal itself — but it takes time: nearly 70 years in this case.\n\n**What\'s next:** Despite the recovery, humpbacks still face threats from ship strikes, fishing net entanglement, and ocean noise pollution from shipping lanes.',
   'Find out which whale species is still critically endangered. What threatens them?',
   'Environment'),

_d('nw003','news','🤖','Kids Are Using AI to Write Code — And Schools Are Responding',
   'Artificial intelligence coding assistants are changing what it means to learn programming.',
   '**What happened:** Tools like GitHub Copilot, Replit AI, and ChatGPT can now write functional computer code from plain English descriptions. Students as young as 10 are using them to build apps, games, and websites with little traditional coding knowledge.\n\n**Why it matters:** This is splitting educators. Some say AI assistants are like calculators for coding — they handle the mechanics so students can focus on problem-solving and creativity. Others worry students are skipping the foundational knowledge they need to debug real-world problems.\n\n**What\'s next:** Many schools are redesigning computer science curricula to teach "AI-assisted coding" as a skill itself — including knowing when to trust AI output and when it gets things wrong.',
   'Try asking a free AI chatbot to write a simple program (like a quiz game). Then try to understand what it wrote.',
   'Tech & Education'),

_d('nw004','news','🌍','A 12-Year-Old Started a Forest That Now Spans 300 Acres',
   'Felix Finkbeiner planted his first tree at age 9. His movement has now planted over 14 billion.',
   '**What happened:** Felix Finkbeiner from Germany was inspired by Wangari Maathai — a Kenyan woman who won the Nobel Peace Prize for planting 30 million trees. At age 9, Felix planted a tree at his school. He founded Plant-for-the-Planet, which grew into a global movement. Today, children in 193 countries have participated in planting over 14 billion trees.\n\n**Why it matters:** Trees absorb carbon dioxide, prevent soil erosion, provide habitat, and cool cities. Forests are one of the most powerful tools against climate change. And Felix proved that young people can drive real global impact.\n\n**What\'s next:** Felix, now in his twenties, is studying environmental science and continues to lead the organisation he started as a child.',
   'Calculate: if one tree absorbs 22 kg of CO₂ per year, how much do 14 billion trees absorb?',
   'Youth Impact'),

_d('nw005','news','🏆','The Youngest Chess Grandmaster in History',
   'Abhimanyu Mishra became a chess Grandmaster at just 12 years, 4 months and 25 days old.',
   '**What happened:** In 2021, American chess prodigy Abhimanyu Mishra broke a record held for 19 years when he earned the Grandmaster title at age 12 — younger than anyone in the history of the game. He had to complete three Grandmaster norms and reach a rating of 2,500 on the FIDE (World Chess Federation) rating system.\n\n**Why it matters:** Chess is considered one of the ultimate tests of strategic thinking, pattern recognition, and memory. Becoming a Grandmaster typically takes decades of dedicated study. Mishra\'s achievement shows what is possible with early passion, the right mentorship, and genuine love for a subject.\n\n**What\'s next:** Mishra continues competing internationally and has a goal of becoming World Champion.',
   'Look up how chess ratings work. What is the difference between a Grandmaster and the World Champion?',
   'Young Achievers'),

_d('nw006','news','🌊','Ocean Temperatures Hit Record Highs Three Years in a Row',
   'The world\'s oceans have never been warmer in recorded history — and scientists are alarmed.',
   '**What happened:** Ocean surface temperatures have broken all-time records for three consecutive years. The North Atlantic in particular has seen temperatures that scientists describe as "off the charts" — far beyond what climate models had predicted for this decade.\n\n**Why it matters:** Oceans absorb about 90% of the extra heat trapped by greenhouse gases. Warmer oceans mean more intense hurricanes and cyclones (warm water is their fuel), bleaching of coral reefs (the Great Barrier Reef suffered its worst bleaching event in 2024), disrupted fish migration patterns, and accelerated ice sheet melting in Greenland and Antarctica.\n\n**What\'s next:** Scientists are calling for faster action to cut emissions before 2030, which they consider a critical tipping point for ocean systems.',
   'Find out what a coral reef bleaching event is and why it is dangerous for ocean life.',
   'Climate'),

_d('nw007','news','🚀','India\'s Chandrayaan-3 Made History on the Moon',
   'India became only the fourth country to land a spacecraft on the Moon — and the first near the south pole.',
   '**What happened:** In August 2023, India\'s Chandrayaan-3 spacecraft successfully landed its Vikram lander and Pragyan rover near the Moon\'s south pole. This made India only the fourth nation (after the USA, USSR, and China) to achieve a soft lunar landing. Russia\'s Luna-25 mission, launched at the same time, crashed.\n\n**Why it matters:** The lunar south pole is of huge scientific interest because ice has been detected there. If large amounts of water ice exist, it could be used by future human missions for drinking water and to produce rocket fuel (by splitting water into hydrogen and oxygen).\n\n**What\'s next:** India plans a follow-up mission and is partnering with NASA\'s Artemis programme, which aims to return humans to the Moon by 2026.',
   'Why is water ice on the Moon so valuable for future space exploration? List three reasons.',
   'Space'),

_d('nw008','news','🎮','Video Games Are Now Officially an Olympic Sport',
   'The International Olympic Committee launched the Olympic Esports Games in 2025.',
   '**What happened:** The International Olympic Committee (IOC) hosted the inaugural Olympic Esports Games in Saudi Arabia in 2025. The event featured 25 games across sports simulations, chess, and other categories, drawing thousands of competitors from over 100 countries.\n\n**Why it matters:** Esports (competitive video gaming) already draws more viewers than many traditional sports. Including it in the Olympic framework gives it global legitimacy and brings in a younger audience. However, some traditional sports fans and athletes question whether gaming should sit alongside physical sports in the Olympics.\n\n**What\'s next:** The format is still evolving. Questions remain about which games qualify, how to handle game updates between competitions, and inclusivity across countries with different tech access.',
   'Should video games be in the Olympics? Write three arguments for and three against.',
   'Sports & Tech'),

_d('nw009','news','🧪','Scientists Create a New Material That Absorbs CO₂ From Air',
   'A new material pulls carbon dioxide directly from the atmosphere — a potential game changer for climate.',
   '**What happened:** Researchers at MIT published results showing a new porous material called "metal-organic frameworks" (MOFs) can capture CO₂ from the air at room temperature using very little energy. It works like a sponge — absorbing CO₂ when cool and releasing a concentrated stream when slightly heated, which can then be stored or converted into fuel.\n\n**Why it matters:** "Direct air capture" of CO₂ is seen as a critical tool for climate action — especially for emissions that are very hard to eliminate (like aviation and agriculture). Current systems are expensive and energy-intensive. A cheaper, more efficient material could make carbon removal economically practical at scale.\n\n**What\'s next:** The team is working on scaling production. They estimate commercial systems using this material could be operating within 5–7 years.',
   'If we can pull CO₂ from the air, should we slow down cutting emissions? Debate both sides.',
   'Climate Science'),

_d('nw010','news','🐘','AI Helps Decode Elephant Communication for the First Time',
   'Scientists used artificial intelligence to identify distinct "words" in elephant calls.',
   '**What happened:** A research team studying African savanna elephants in Kenya used machine learning to analyse thousands of elephant vocalisations. The AI identified patterns suggesting elephants use specific sounds to address individual other elephants — essentially using names. When researchers played back name-calls, elephants responded specifically to their own name-calls more than to others.\n\n**Why it matters:** If confirmed, this would make elephants only the second non-human species (after dolphins) known to use individualised names. It suggests elephant communication is far more sophisticated than previously understood and could change how we think about animal intelligence and rights.\n\n**What\'s next:** The team is creating a comprehensive database of elephant calls across different herds and regions to understand vocabulary and regional "dialects."',
   'What other animals do scientists think have complex communication? Research dolphin language.',
   'Animal Science'),

_d('nw011','news','💊','New Malaria Vaccine Reaches 90% Effectiveness in Trials',
   'A next-generation malaria vaccine has shown unprecedented results in clinical trials.',
   '**What happened:** The R21/Matrix-M malaria vaccine, developed by Oxford University and manufactured by the Serum Institute of India, showed up to 90% effectiveness in Phase 3 trials across Africa. It has now been approved for use in several African countries and is being produced at scale.\n\n**Why it matters:** Malaria kills over 600,000 people per year — mostly children under five in sub-Saharan Africa. Despite decades of research, no vaccine had exceeded 50% effectiveness until now. This breakthrough could save hundreds of thousands of lives annually.\n\n**What\'s next:** The Gates Foundation is funding distribution efforts. The goal is to vaccinate children across 40 countries by 2030. Delivery logistics — keeping vaccines cold across remote areas — remains a major challenge.',
   'Calculate how many lives could be saved in 10 years if this vaccine prevents 500,000 deaths per year.',
   'Health'),

_d('nw012','news','🏗️','The World\'s Largest Vertical Farm Opens in the UAE',
   'A football-field-sized farm growing crops in stacked indoor layers without soil or sunlight.',
   '**What happened:** A 330,000 square foot vertical farm opened in Dubai, UAE — one of the world\'s driest places. It grows leafy greens, herbs, and strawberries using 95% less water than conventional farming, zero pesticides, and LED lighting instead of sunlight. The crops grow in stacked layers in a controlled environment year-round, regardless of desert heat.\n\n**Why it matters:** With the world\'s population heading toward 10 billion, and climate change making traditional farming harder in many regions, vertical farming offers a path to food security in difficult environments. The UAE currently imports 80-90% of its food — this farm is part of a national strategy for self-sufficiency.\n\n**What\'s next:** The company plans to open farms in Singapore, the UK, and the USA within three years.',
   'What are the advantages and disadvantages of vertical farming compared to traditional farming?',
   'Future of Food'),

_d('nw013','news','🧠','Brain Implant Lets Paralysed Man Walk Again Using Thought',
   'A wireless brain-computer interface restored leg movement in a man paralysed for 12 years.',
   '**What happened:** Scientists in Switzerland implanted two wireless devices — one in the brain, one in the spine — in a man paralysed from a bicycle accident 12 years earlier. The brain device reads movement intentions; the spinal device stimulates leg muscles to execute them. After training, the man could walk up to 500 metres, climb stairs, and even stand at a bar for a drink.\n\n**Why it matters:** This "digital bridge" bypasses the severed spinal cord using artificial signals. It does not restore sensation, but it restores voluntary movement — something once considered impossible for complete spinal injuries. The patient described it as being able to "feel human again."\n\n**What\'s next:** The system requires a surgical implant and extensive rehabilitation. The team is working on making it smaller, wireless, and faster to set up.',
   'What ethical questions arise when computers are permanently connected to human brains?',
   'Medical Tech'),

_d('nw014','news','📚','Reading Fiction Makes You a Better Person — Science Confirms It',
   'Reading novels measurably increases empathy, social intelligence, and emotional understanding.',
   '**What happened:** A meta-analysis published in a leading psychology journal reviewed 114 studies on reading fiction and found consistent, significant improvements in empathy and "theory of mind" (the ability to understand that others have different thoughts and feelings). The effect was strongest in children and adolescents who read regularly.\n\n**Why it matters:** In a world increasingly polarised, empathy is a social superpower. Fiction forces readers to inhabit other minds — understanding why characters do things, feeling their emotions, seeing the world from perspectives completely unlike their own. Non-fiction, by contrast, showed far weaker effects on empathy measures.\n\n**What\'s next:** Several school systems are using this research to justify keeping fiction central to the curriculum despite pressure to focus on "practical" STEM subjects.',
   'Think of a book that changed how you see a person or group. How did it change your view?',
   'Reading Science'),

_d('nw015','news','🌱','Country-Sized Area of Forest Regrows Naturally in Brazil',
   'Natural forest regeneration — without planting a single tree — is recovering millions of hectares.',
   '**What happened:** Satellite analysis published by researchers at MapBiomas found that over 4.2 million hectares of forest in Brazil spontaneously regrew between 2000 and 2023 on land that had been cleared for agriculture then abandoned. This is roughly the size of the Netherlands — without anyone planting a single tree.\n\n**Why it matters:** Natural forest regeneration is significantly cheaper than planting trees and often produces more biodiverse, resilient forest. This challenges the idea that restoring forests always requires expensive human intervention. Simply stopping deforestation and allowing nature to work is often the most powerful tool available.\n\n**What\'s next:** Scientists argue this finding should shift reforestation funding toward protecting existing regenerating forests, not just planting campaigns.',
   'Compare the cost and biodiversity of natural forest regeneration versus tree-planting programmes.',
   'Environment'),

_d('nw016','news','🎒','Solar Panel Backpack Charges Student Devices',
   'A teenage inventor created a backpack that turns sunlight into phone and laptop power.',
   '**What happened:** A 16-year-old student in Kenya designed a backpack with flexible solar panels sewn into the fabric. It stores energy in a small battery that can charge phones, tablets, and LED lamps. He was inspired by power outages that interrupted his homework.\n\n**Why it matters:** In many parts of the world, reliable electricity is not guaranteed. A solar backpack provides portable power for studying after dark. It also reduces reliance on polluting diesel generators and kerosene lamps.\n\n**What\'s next:** The inventor is working with local manufacturers to produce affordable versions for students across rural Africa.',
   'List three everyday objects you could power with a small solar panel.'),

_d('nw017','news','🌳','Old Subway Tunnel Becomes Underground Park',
   'A city transformed an abandoned train tunnel into a green public space.',
   '**What happened:** Urban planners in a major European city opened a new underground park inside a disused subway tunnel. The space uses LED grow lights, hydroponic planters, and recycled rainwater to grow vegetables and flowers year-round. Locals can visit, volunteer, and even buy fresh produce.\n\n**Why it matters:** Cities often have unused underground spaces. Turning them into parks adds greenery, improves air quality, and creates community gathering places without taking up street-level land.\n\n**What\'s next:** Other cities are studying the project to see if similar tunnels, bunkers, and abandoned spaces can be reused.',
   'What unused space in your town could be turned into something useful?'),

_d('nw018','news','💧','Teen Invents Cheap Lead Detector for Tap Water',
   'A 15-year-old created a device that warns families if their drinking water contains lead.',
   '**What happened:** A high school student developed a small, inexpensive sensor that changes color when lead is present in water. Traditional lead tests require sending samples to a lab and cost much more. Her device can give results in minutes using materials that cost under $5.\n\n**Why it matters:** Lead in drinking water can harm brain development, especially in children. Many older pipes still contain lead, and not all communities can afford frequent testing. A cheap, fast test could help families protect themselves.\n\n**What\'s next:** The student is partnering with water safety organizations to test the device in real homes and refine it for mass production.',
   'Why is detecting lead in water especially important for young children?'),

_d('nw019','news','📚','Library on Wheels Brings Books to Remote Villages',
   'A bicycle-powered library is delivering books to children who have no local library.',
   '**What happened:** A teacher in a rural region converted a cargo bicycle into a mobile library. Several times a week, she pedals to different villages and lets children borrow books. The project started with just 50 donated books and has grown to over 5,000.\n\n**Why it matters:** Access to books is one of the strongest predictors of reading success and school achievement. Children in remote areas often have no library nearby. A mobile library brings stories, knowledge, and joy directly to them.\n\n**What\'s next:** The project is fundraising for electric cargo bikes and e-readers to reach even more villages.',
   'What book would you donate to a mobile library for kids your age?'),

_d('nw020','news','♻️','Young Coder Builds App to Simplify Recycling',
   'A 14-year-old created an app that tells you exactly how to recycle any item.',
   '**What happened:** Frustrated by confusing recycling rules, a teenager built a free app where users scan a barcode or type an item name to learn whether it is recyclable, compostable, or landfill. The app also shows the nearest recycling drop-off locations.\n\n**Why it matters:** Different cities have different recycling rules, and many people accidentally contaminate recycling bins with non-recyclable items. Clear guidance can dramatically reduce waste sent to landfills.\n\n**What\'s next:** The app is expanding to include repair guides and upcycling ideas so items stay useful longer.',
   'Pick one item in your home and research the correct way to dispose of it locally.'),
]

# ── Flat pool for rotation ─────────────────────────────────────────────────────
ALL_ITEMS = {item['id']: item for item in SPACE + MANNERS + FUNFACTS + HACKS + GAMES + TRENDING + NEWS}

CATEGORY_POOLS = {
    'space':    SPACE,
    'manners':  MANNERS,
    'funfact':  FUNFACTS,
    'hack':     HACKS,
    'game':     GAMES,
    'trending': TRENDING,
    'news':     NEWS,
}

CATEGORY_META = {
    'space':    {'label': 'Space Explorer', 'emoji': '🚀', 'color': '#1e1b4b', 'bg': '#ede9fe'},
    'manners':  {'label': 'Life Skills',    'emoji': '🤝', 'color': '#14532d', 'bg': '#dcfce7'},
    'funfact':  {'label': 'Fun Facts',      'emoji': '🤯', 'color': '#7c2d12', 'bg': '#ffedd5'},
    'hack':     {'label': '2-Min Hacks',    'emoji': '⚡', 'color': '#0c4a6e', 'bg': '#e0f2fe'},
    'game':     {'label': 'Brain Games',    'emoji': '🎮', 'color': '#4c1d95', 'bg': '#f5f3ff'},
    'trending': {'label': 'Trending Now',   'emoji': '📈', 'color': '#881337', 'bg': '#fff1f2'},
    'news':     {'label': 'Kids News',      'emoji': '📰', 'color': '#1e3a5f', 'bg': '#dbeafe'},
}

ORDERED_CATEGORIES = ['space', 'manners', 'funfact', 'hack', 'game', 'trending', 'news']


def get_daily_item(category: str, seen_ids: list) -> dict | None:
    """Return today's item for a category using date seeding, avoiding seen IDs."""
    pool = CATEGORY_POOLS.get(category, [])
    if not pool:
        return None
    today_seed = int(date.today().strftime('%Y%m%d'))
    unseen = [item for item in pool if item['id'] not in seen_ids]
    if not unseen:
        unseen = pool  # reset when all seen
    rng = random.Random(today_seed + hash(category))
    return rng.choice(unseen)


def get_item_by_id(item_id: str) -> dict | None:
    return ALL_ITEMS.get(item_id)
