import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, Video
from django.utils.text import slugify

def populate_with_ultimate_cbse_data():
    print("Clearing old data...")
    Grade.objects.all().delete()
    print("Starting ultimate comprehensive CBSE data population...")

    cbse_data = {
        'NDA': {
            'Maths': ['Algebra', 'Matrices and Determinants', 'Trigonometry', 'Analytical Geometry', 'Differential Calculus', 'Integral Calculus', 'Vector Algebra', 'Statistics and Probability'],
            'English': ['Grammar and Usage', 'Vocabulary', 'Comprehension', 'Cohesion in Extended Text'],
            'Physics': ['Properties of Matter', 'Mechanics', 'Heat and Thermodynamics', 'Sound', 'Optics', 'Electromagnetism'],
            'Chemistry': ['Physical and Chemical Changes', 'Elements and Compounds', 'Acids, Bases and Salts', 'Atomic Structure'],
            'Science': ['Difference between Living and Non-living', 'Cells', 'Human Body', 'Food and Balanced Diet', 'Solar System'],
            'Social Science': ['Indian History', 'Freedom Movement', 'Constitution of India', 'Geography of India and World', 'Current Events']
        },
        'JEE': {
            'Physics': ['Mechanics', 'Thermodynamics', 'Electromagnetism', 'Optics', 'Modern Physics', 'Properties of Matter'],
            'Chemistry': ['Physical Chemistry', 'Inorganic Chemistry', 'Organic Chemistry', 'Environmental Chemistry', 'Biomolecules and Polymers'],
            'Maths': ['Algebra', 'Trigonometry', 'Coordinate Geometry', 'Calculus', 'Vectors and 3D Geometry', 'Statistics and Probability']
        },
        'NEET': {
            'Physics': ['Mechanics', 'Thermodynamics', 'Electromagnetism', 'Optics', 'Modern Physics', 'Kinematics', 'Laws of Motion'],
            'Chemistry': ['Physical Chemistry', 'Inorganic Chemistry', 'Organic Chemistry', 'Equilibrium', 'Structure of Atom'],
            'Biology': ['Diversity in Living World', 'Structural Organisation in Animals and Plants', 'Cell Structure and Function', 'Plant Physiology', 'Human Physiology', 'Reproduction', 'Genetics and Evolution', 'Biology and Human Welfare', 'Biotechnology and Its Applications', 'Ecology and Environment']
        },
        'Class 12': {
            'Physics': ['Electric Charges and Fields', 'Electrostatic Potential and Capacitance', 'Current Electricity', 'Moving Charges and Magnetism', 'Magnetism and Matter', 'Electromagnetic Induction', 'Alternating Current', 'Electromagnetic Waves', 'Ray Optics and Optical Instruments', 'Wave Optics', 'Dual Nature of Radiation and Matter', 'Atoms', 'Nuclei', 'Semiconductor Electronics'],
            'Chemistry': ['The Solid State', 'Solutions', 'Electrochemistry', 'Chemical Kinetics', 'Surface Chemistry', 'General Principles and Processes of Isolation of Elements', 'The p-Block Elements', 'The d and f Block Elements', 'Coordination Compounds', 'Haloalkanes and Haloarenes', 'Alcohols Phenols and Ethers', 'Aldehydes Ketones and Carboxylic Acids', 'Amines', 'Biomolecules', 'Polymers', 'Chemistry in Everyday Life'],
            'Maths': ['Relations and Functions', 'Inverse Trigonometric Functions', 'Matrices', 'Determinants', 'Continuity and Differentiability', 'Application of Derivatives', 'Integrals', 'Application of Integrals', 'Differential Equations', 'Vector Algebra', 'Three Dimensional Geometry', 'Linear Programming', 'Probability'],
            'Biology': ['Reproduction in Organisms', 'Sexual Reproduction in Flowering Plants', 'Human Reproduction', 'Reproductive Health', 'Principles of Inheritance and Variation', 'Molecular Basis of Inheritance', 'Evolution', 'Human Health and Disease', 'Strategies for Enhancement in Food Production', 'Microbes in Human Welfare', 'Biotechnology: Principles and Processes', 'Biotechnology and its Applications', 'Organisms and Populations', 'Ecosystem', 'Biodiversity and Conservation', 'Environmental Issues'],
            'Accountancy': ['Accounting for Not-for-Profit Organisation', 'Accounting for Partnership: Basic Concepts', 'Reconstitution of a Partnership Firm', 'Dissolution of Partnership Firm', 'Accounting for Share Capital', 'Issue and Redemption of Debentures', 'Financial Statements of a Company', 'Analysis of Financial Statements', 'Accounting Ratios', 'Cash Flow Statement'],
            'Business Studies': ['Nature and Significance of Management', 'Principles of Management', 'Business Environment', 'Planning', 'Organising', 'Staffing', 'Directing', 'Controlling', 'Financial Management', 'Financial Markets', 'Marketing Management', 'Consumer Protection'],
            'Economics': ['Introduction to Macroeconomics', 'National Income Accounting', 'Money and Banking', 'Determination of Income and Employment', 'Government Budget and the Economy', 'Open Economy Macroeconomics', 'Indian Economic Development'],
            'Computer Science': ['Python Revision Tour', 'Python Revision Tour II', 'Functions', 'Using Python Libraries', 'File Handling', 'Recursion', 'Idea of Algorithmic Efficiency', 'Data Structures', 'Computer Networks', 'Django', 'Relational Databases', 'Simple Queries in SQL', 'Table Creation and Data Manipulation Commands', 'Grouping Records, Joins in SQL', 'Interface of Python with an SQL Database'],
            'English': ['The Last Lesson', 'Lost Spring', 'Deep Water', 'The Rattrap', 'Indigo', 'Poets and Pancakes', 'The Interview', 'Going Places', 'My Mother at Sixty-six', 'Keeping Quiet', 'A Thing of Beauty', 'A Roadside Stand', 'Aunt Jennifer\'s Tigers']
        },
        'Class 11': {
            'Physics': ['Physical World', 'Units and Measurements', 'Motion in a Straight Line', 'Motion in a Plane', 'Laws of Motion', 'Work Energy and Power', 'System of Particles and Rotational Motion', 'Gravitation', 'Mechanical Properties of Solids', 'Mechanical Properties of Fluids', 'Thermal Properties of Matter', 'Thermodynamics', 'Kinetic Theory', 'Oscillations', 'Waves'],
            'Chemistry': ['Some Basic Concepts of Chemistry', 'Structure of Atom', 'Classification of Elements', 'Chemical Bonding and Molecular Structure', 'States of Matter', 'Thermodynamics', 'Equilibrium', 'Redox Reactions', 'Hydrogen', 'The s-Block Elements', 'The p-Block Elements', 'Organic Chemistry: Some Basic Principles and Techniques', 'Hydrocarbons', 'Environmental Chemistry'],
            'Maths': ['Sets', 'Relations and Functions', 'Trigonometric Functions', 'Principle of Mathematical Induction', 'Complex Numbers and Quadratic Equations', 'Linear Inequalities', 'Permutations and Combinations', 'Binomial Theorem', 'Sequence and Series', 'Straight Lines', 'Conic Sections', 'Introduction to Three Dimensional Geometry', 'Limits and Derivatives', 'Mathematical Reasoning', 'Statistics', 'Probability'],
            'Biology': ['The Living World', 'Biological Classification', 'Plant Kingdom', 'Animal Kingdom', 'Morphology of Flowering Plants', 'Anatomy of Flowering Plants', 'Structural Organisation in Animals', 'Cell: The Unit of Life', 'Biomolecules', 'Cell Cycle and Cell Division', 'Transport in Plants', 'Mineral Nutrition', 'Photosynthesis in Higher Plants', 'Respiration in Plants', 'Plant Growth and Development', 'Digestion and Absorption', 'Breathing and Exchange of Gases', 'Body Fluids and Circulation', 'Excretory Products and their Elimination', 'Locomotion and Movement', 'Neural Control and Coordination', 'Chemical Coordination and Integration'],
            'Accountancy': ['Introduction to Accounting', 'Theory Base of Accounting', 'Recording of Transactions - I', 'Recording of Transactions - II', 'Bank Reconciliation Statement', 'Trial Balance and Rectification of Errors', 'Depreciation Provisions and Reserves', 'Bill of Exchange', 'Financial Statements - I', 'Financial Statements - II', 'Accounts from Incomplete Records', 'Applications of Computers in Accounting', 'Computerised Accounting System'],
            'Business Studies': ['Business Trade and Commerce', 'Forms of Business Organisation', 'Private Public and Global Enterprises', 'Business Services', 'Emerging Modes of Business', 'Social Responsibilities of Business and Business Ethics', 'Formation of a Company', 'Sources of Business Finance', 'Small Business and Enterprises', 'Internal Trade', 'International Business'],
            'Economics': ['Introduction to Microeconomics', 'Theory of Consumer Behaviour', 'Production and Costs', 'The Theory of the Firm under Perfect Competition', 'Market Equilibrium', 'Non-Competitive Markets', 'Statistics for Economics'],
            'Computer Science': ['Computer System Overview', 'Data Representation', 'Boolean Logic', 'Insight Into Program Execution', 'Relational Databases', 'Simple Queries in SQL', 'Table Creation and Data Manipulation Commands', 'Cyber Safety', 'Getting Started with Python', 'Python Fundamentals', 'Data Handling', 'Conditional and Iterative Statements', 'String Manipulation', 'List Manipulation', 'Tuples', 'Dictionaries', 'Understanding Sorting'],
            'English': ['The Portrait of a Lady', 'A Photograph', 'We\'re Not Afraid to Die... if We Can All Be Together', 'Discovering Tut: the Saga Continues', 'The Laburnum Top', 'The Voice of the Rain', 'Childhood', 'The Adventure', 'Silk Road', 'Father to Son']
        },
        'Class 10': {
            'Maths': ['Real Numbers', 'Polynomials', 'Pair of Linear Equations in Two Variables', 'Quadratic Equations', 'Arithmetic Progressions', 'Triangles', 'Coordinate Geometry', 'Introduction to Trigonometry', 'Some Applications of Trigonometry', 'Circles', 'Constructions', 'Areas Related to Circles', 'Surface Areas and Volumes', 'Statistics', 'Probability'],
            'Science': ['Chemical Reactions and Equations', 'Acids, Bases and Salts', 'Metals and Non-metals', 'Carbon and its Compounds', 'Periodic Classification of Elements', 'Life Processes', 'Control and Coordination', 'How do Organisms Reproduce?', 'Heredity and Evolution', 'Light Reflection and Refraction', 'Human Eye and Colourful World', 'Electricity', 'Magnetic Effects of Electric Current', 'Sources of Energy', 'Our Environment', 'Sustainable Management of Natural Resources'],
            'Social Science': ['The Rise of Nationalism in Europe', 'Nationalism in India', 'The Making of a Global World', 'The Age of Industrialisation', 'Print Culture and the Modern World', 'Resources and Development', 'Forest and Wildlife Resources', 'Water Resources', 'Agriculture', 'Minerals and Energy Resources', 'Manufacturing Industries', 'Lifelines of National Economy', 'Power Sharing', 'Federalism', 'Democracy and Diversity', 'Gender, Religion and Caste', 'Popular Struggles and Movements', 'Political Parties', 'Outcomes of Democracy', 'Challenges to Democracy', 'Development', 'Sectors of the Indian Economy', 'Money and Credit', 'Globalisation and the Indian Economy', 'Consumer Rights'],
            'English': ['A Letter to God', 'Nelson Mandela: Long Walk to Freedom', 'Two Stories about Flying', 'From the Diary of Anne Frank', 'The Hundred Dresses - I', 'The Hundred Dresses - II', 'Glimpses of India', 'Mijbil the Otter', 'Madam Rides the Bus', 'The Sermon at Benares', 'The Proposal'],
            'Hindi': ['Surdas Ke Pad', 'Ram-Lakshman-Parashuram Samvad', 'Savaiya and Kavitt', 'Atmakathya', 'Utsaha and At Ni Rahi Hai', 'Yeh Danturit Muskan and Fasal', 'Chhaya Mat Chhuna', 'Kanyadaan', 'Sangatkar'],
            'Information Technology': ['Digital Documentation (Advanced)', 'Electronic Spreadsheet (Advanced)', 'Database Management System', 'Web Applications and Security']
        },
        'Class 9': {
            'Maths': ['Number Systems', 'Polynomials', 'Coordinate Geometry', 'Linear Equations in Two Variables', 'Introduction to Euclid’s Geometry', 'Lines and Angles', 'Triangles', 'Quadrilaterals', 'Areas of Parallelograms and Triangles', 'Circles', 'Constructions', 'Heron’s Formula', 'Surface Areas and Volumes', 'Statistics', 'Probability'],
            'Science': ['Matter in Our Surroundings', 'Is Matter Around Us Pure', 'Atoms and Molecules', 'Structure of the Atom', 'The Fundamental Unit of Life', 'Tissues', 'Diversity in Living Organisms', 'Motion', 'Force and Laws of Motion', 'Gravitation', 'Work and Energy', 'Sound', 'Why Do We Fall Ill', 'Natural Resources', 'Improvement in Food Resources'],
            'Social Science': ['The French Revolution', 'Socialism in Europe and the Russian Revolution', 'Nazism and the Rise of Hitler', 'Forest Society and Colonialism', 'Pastoralists in the Modern World', 'India - Size and Location', 'Physical Features of India', 'Drainage', 'Climate', 'Natural Vegetation and Wildlife', 'Population', 'What is Democracy? Why Democracy?', 'Constitutional Design', 'Electoral Politics', 'Working of Institutions', 'Democratic Rights', 'The Story of Village Palampur', 'People as Resource', 'Poverty as a Challenge', 'Food Security in India'],
            'English': ['The Fun They Had', 'The Sound of Music', 'The Little Girl', 'A Truly Beautiful Mind', 'The Snake and the Mirror', 'My Childhood', 'Packing', 'Reach for the Top', 'The Bond of Love', 'Kathmandu', 'If I Were You'],
            'Hindi': ['Do Bailon Ki Katha', 'Lhasa Ki Aur', 'Upbhoktavad Ki Sanskriti', 'Sanwale Sapnon Ki Yaad', 'Nana Saheb Ki Putri', 'Premchand Ke Phate Joote', 'Mere Bachpan Ke Din', 'Ek Kutta Aur Ek Maina', 'Sakhian Evam Sabad', 'Vaakh'],
            'Information Technology': ['Introduction to IT-ITeS Industry', 'Data Entry & Keyboarding Skills', 'Digital Documentation', 'Electronic Spreadsheet', 'Digital Presentation']
        },
        'Class 8': {
            'Maths': ['Rational Numbers', 'Linear Equations in One Variable', 'Understanding Quadrilaterals', 'Practical Geometry', 'Data Handling', 'Squares and Square Roots', 'Cubes and Cube Roots', 'Comparing Quantities', 'Algebraic Expressions and Identities', 'Visualising Solid Shapes', 'Mensuration', 'Exponents and Powers', 'Direct and Inverse Proportions', 'Factorisation', 'Introduction to Graphs', 'Playing with Numbers'],
            'Science': ['Crop Production and Management', 'Microorganisms: Friend and Foe', 'Synthetic Fibres and Plastics', 'Materials: Metals and Non-Metals', 'Coal and Petroleum', 'Combustion and Flame', 'Conservation of Plants and Animals', 'Cell: Structure and Functions', 'Reproduction in Animals', 'Reaching the Age of Adolescence', 'Force and Pressure', 'Friction', 'Sound', 'Chemical Effects of Electric Current', 'Some Natural Phenomena', 'Light', 'Stars and the Solar System', 'Pollution of Air and Water'],
            'Social Science': ['How, When and Where', 'From Trade to Territory', 'Ruling the Countryside', 'Tribals, Dikus and the Vision of a Golden Age', 'When People Rebel 1857 and After', 'Colonialism and the City', 'Weavers, Iron Smelters and Factory Owners', 'Civilising the Native, Educating the Nation', 'Women, Caste and Reform', 'The Changing World of Visual Arts', 'The Making of the National Movement 1870s-1947', 'India After Independence'],
            'English': ['The Best Christmas Present in the World', 'The Tsunami', 'Glimpses of the Past', 'Bepin Choudhury’s Lapse of Memory', 'The Summit Within', 'This is Jody’s Fawn', 'A Visit to Cambridge', 'A Short Monsoon Diary', 'The Great Stone Face - I', 'The Great Stone Face - II'],
            'Hindi': ['Dhwani', 'Lakh Ki Chudiyan', 'Bus Ki Yatra', 'Diwanon Ki Hasti', 'Chitthiyon Ki Anoothi Duniya', 'Bhagwan Ke Dakiye', 'Kya Nirash Hua Jaye', 'Yeh Sabse Kathin Samay Nahi', 'Kabir Ki Sakhiyan', 'Kaamchor', 'Jab Cinema Ne Bolna Seekha', 'Sudama Charit', 'Jahan Pahiya Hai', 'Akbari Lota', 'Sur Ke Pad', 'Pani Ki Kahani', 'Baaz Aur Saanp', 'Topi'],
            'Sanskrit': ['Subhashitani', 'Bilasya Vani Na Kadapi Me Shruta', 'Digibharatam', 'Sadaiva Purato Nidhehi Charanam', 'Kantakenaiva Kantakam', 'Griham Shunyam Sutam Vina', 'Bharatajanataham', 'Sansarasagarasya Nayakah', 'Saptabhaginyah', 'Nitinavanitam', 'Savitribai Phule', 'Kah Rakshati Kah Rakshitah', 'Kshitau Rajate Bharatashwarnabhumi', 'Aryabhatah']
        },
        'Class 7': {
            'Maths': ['Integers', 'Fractions and Decimals', 'Data Handling', 'Simple Equations', 'Lines and Angles', 'The Triangle and its Properties', 'Congruence of Triangles', 'Comparing Quantities', 'Rational Numbers', 'Practical Geometry', 'Perimeter and Area', 'Algebraic Expressions', 'Exponents and Powers', 'Symmetry', 'Visualising Solid Shapes'],
            'Science': ['Nutrition in Plants', 'Nutrition in Animals', 'Fibre to Fabric', 'Heat', 'Acids, Bases and Salts', 'Physical and Chemical Changes', 'Weather, Climate and Adaptations of Animals to Climate', 'Winds, Storms and Cyclones', 'Soil', 'Respiration in Organisms', 'Transportation in Animals and Plants', 'Reproduction in Plants', 'Motion and Time', 'Electric Current and its Effects', 'Light', 'Water: A Precious Resource', 'Forests: Our Lifeline', 'Wastewater Story'],
            'Social Science': ['Tracing Changes Through a Thousand Years', 'New Kings and Kingdoms', 'The Delhi Sultans', 'The Mughal Empire', 'Rulers and Buildings', 'Towns, Traders and Craftspersons', 'Tribes, Nomads and Settled Communities', 'Devotional Paths to the Divine', 'The Making of Regional Cultures', 'Eighteenth-Century Political Formations'],
            'English': ['Three Questions', 'A Gift of Chappals', 'Gopal and the Hilsa Fish', 'The Ashes That Made Trees Bloom', 'Quality', 'Expert Detectives', 'The Invention of Vita-Wonk', 'Fire: Friend and Foe', 'A Bicycle in Good Repair', 'The Story of Cricket'],
            'Hindi': ['Hum Panchhi Unmukt Gagan Ke', 'Dadi Maa', 'Himalaya Ki Betiyan', 'Kathputli', 'Mithaiwala', 'Rakt Aur Hamara Sharir', 'Papa Kho Gaye', 'Shaam Ek Kisan', 'Chidiya Ki Bachi', 'Apoorv Anubhav', 'Rahim Ke Dohe', 'Kancha', 'Ek Tinka', 'Khanpan Ki Badalti Tasveer', 'Neelkanth', 'Bhor Aur Barkha', 'Veer Kunwar Singh', 'Sangharsh Ke Karan Main Tunukmizaj Ho Gaya', 'Ashram Ka Anumanit Vyay', 'Viplav Gayan'],
            'Sanskrit': ['Subhashitani', 'Durbuddhi Vinashyati', 'Svavalambanam', 'Pandyita Ramabai', 'Sadacharah', 'Sankalpah Siddhidhayakah', 'Trivarnah Dhvajah', 'Aham Api Vidyalayam Gamishyami', 'Vishvabandhutvam', 'Samavayo Hi Durjayah', 'Vidyadhanam', 'Amritam Samskritam', 'Lalangitam']
        },
        'Class 6': {
            'Maths': ['Knowing Our Numbers', 'Whole Numbers', 'Playing with Numbers', 'Basic Geometrical Ideas', 'Understanding Elementary Shapes', 'Integers', 'Fractions', 'Decimals', 'Data Handling', 'Mensuration', 'Algebra', 'Ratio and Proportion', 'Symmetry', 'Practical Geometry'],
            'Science': ['Food: Where Does it Come From?', 'Components of Food', 'Fibre to Fabric', 'Sorting Materials into Groups', 'Separation of Substances', 'Changes Around Us', 'Getting to Know Plants', 'Body Movements', 'The Living Organisms and Their Surroundings', 'Motion and Measurement of Distances', 'Light, Shadows and Reflections', 'Electricity and Circuits', 'Fun with Magnets', 'Water', 'Air Around Us', 'Garbage In, Garbage Out'],
            'Social Science': ['What, Where, How and When?', 'On The Trail of the Earliest People', 'From Gathering to Growing Food', 'In the Earliest Cities', 'What Books and Burials Tell Us', 'Kingdoms, Kings and an Early Republic', 'New Questions and Ideas', 'Ashoka, The Emperor Who Gave Up War', 'Vital Villages, Thriving Towns', 'Traders, Kings and Pilgrims', 'New Empires and Kingdoms', 'Buildings, Paintings and Books'],
            'English': ['Who Did Patrick’s Homework?', 'How the Dog Found Himself a New Master?', 'Taro’s Reward', 'An Indian – American Woman in Space: Kalpana Chawla', 'A Different Kind of School', 'Who I Am', 'Fair Play', 'A Game of Chance', 'Desert Animals', 'The Banyan Tree'],
            'Hindi': ['Vah Chidiya Jo', 'Bachpan', 'Nadan Dost', 'Chand se Thodi Si Gappe', 'Aksharon Ka Mahatva', 'Paar Nazar Ke', 'Sathi Hath Badhana', 'Aise Aise', 'Ticket Album', 'Jhansi ki Rani', 'Jo Dekhkar Bhi Nahi Dekhte', 'Sansar Pustak Hai', 'Main Sabse Chhoti Houn', 'Lokgeet', 'Naukar', 'Van Ke Marg Mein', 'Saans-Saans Mein Bans'],
            'Sanskrit': ['Shabdaparichayah I', 'Shabdaparichayah II', 'Shabdaparichayah III', 'Vidyalayah', 'Vrikshah', 'Samudratatah', 'Bakasya Pratikarah', 'Suktistabakah', 'Kridaspardha', 'Krishikah Karmavirah', 'Dashamah Tvam Asi', 'Vimanayanam Rachayama', 'Ahaha Aah Cha']
        },
        'Class 5': {
            'Maths': ['The Fish Tale', 'Shapes and Angles', 'How Many Squares?', 'Parts and Wholes', 'Does it Look the Same?', 'Be My Multiple, I’ll be Your Factor', 'Can You See the Pattern?', 'Mapping Your Way', 'Boxes and Sketches', 'Tenths and Hundredths', 'Area and its Boundary', 'Smart Charts', 'Ways to Multiply and Divide', 'How Big? How Heavy?'],
            'EVS': ['Super Senses', 'A Snake Charmer’s Story', 'From Tasting to Digesting', 'Mangoes Round the Year', 'Seeds and Seeds', 'Every Drop Counts', 'Experiments with Water', 'A Treat for Mosquitoes', 'Up You Go!', 'Walls Tell Stories', 'Sunita in Space', 'What if it Finishes...?', 'A Shelter so High!', 'When the Earth Shook!', 'Blow Hot, Blow Cold', 'Who will do this Work?', 'Across the Wall', 'No Place for Us?', 'A Seed tells a Farmer’s Story', 'Whose Forests?', 'Like Father, Like Daughter', 'On the Move Again'],
            'English': ['Ice-cream Man', 'Wonderful Waste!', 'Teamwork', 'Flying Together', 'My Shadow', 'Robinson Crusoe Discovers a footprint', 'Crying', 'My Elder Brother', 'The Lazy Frog', 'Rip Van Winkle', 'Class Discussion', 'The Talkative Barber', 'Topsy-turvy Land', 'Gulliver’s Travels', 'Nobody’s Friend', 'The Little Bully', 'Sing a Song of People', 'Around the World', 'Malu Bhalu', 'Who Will be Ningthou?'],
            'Hindi': ['Raakh Ki Rassi', 'Faslon Ke Tyohar', 'Khilone Wala', 'Nanh Fankar', 'Jahan Chah Wahan Raah', 'Chitthi Ka Safar', 'Ve Din Bhi Kya Din The', 'Ek Maa Ki Bebasi', 'Ek Din Ki Badshahat', 'Chawal Ki Rotiyan', 'Guru Aur Chela', 'Swami Ki Dadi', 'Bagh Aaya Us Raat', 'Bishan Ki Dileri', 'Pani Re Pani', 'Chhoti Si Hamari Nadi', 'Chunauti Himalay Ki']
        },
        'Class 4': {
            'Maths': ['Building with Bricks', 'Long and Short', 'A Trip to Bhopal', 'Tick-Tick-Tick', 'The Way The World Looks', 'The Junk Seller', 'Jugs and Mugs', 'Carts and Wheels', 'Halves and Quarters', 'Play with Patterns', 'Tables and Shares', 'How Heavy? How Light?', 'Fields and Fences', 'Smart Charts'],
            'EVS': ['Going to School', 'Ear to Ear', 'A Day with Nandu', 'The Story of Amrita', 'Anita and the Honeybees', 'Omana’s Journey', 'From the Window', 'Reaching Grandmother’s House', 'Changing Families', 'Hu Tu Tu, Hu Tu Tu', 'The Valley of Flowers', 'Changing Times', 'A River’s Tale', 'Basva’s Farm', 'From Market to Home', 'A Busy Month', 'Nandita in Mumbai', 'Too Much Water, Too Little Water', 'Abdul in the Garden', 'Eating Together', 'Food and Fun', 'The World in my Home', 'Pochampalli', 'Home and Abroad', 'Spicy Riddles', 'Defence Officer: Wahida', 'Chuskit Goes to School'],
            'English': ['Wake Up!', 'Neha’s Alarm Clock', 'Noses', 'The Little Fir Tree', 'Run!', 'Nasruddin’s Aim', 'Why?', 'Alice in Wonderland', 'Don’t be Afraid of the Dark', 'Helen Keller', 'The Milkman’s Cow', 'Hiawatha', 'The Scholar’s Mother Tongue', 'A Watering Rhyme', 'The Giving Tree', 'The Going to Buy a Book', 'Pinocchio'],
            'Hindi': ['Man Ke Bhole Bhale Badal', 'Jaisa Sawal Waisa Jawab', 'Kirmich Ki Gend', 'Papa Jab Bachche The', 'Dost Ki Poshak', 'Naav Banao Naav Banao', 'Daan Ka Hisab', 'Kaun', 'Swatantrata Ki Oar', 'Thapp Roti Thapp Dal', 'Padhakku Ki Soojh', 'Sunita Ki Pahiya Kursi', 'Hudhud', 'Muft Hi Muft']
        },
        'Class 3': {
            'Maths': ['Where to Look From', 'Fun with Numbers', 'Give and Take', 'Long and Short', 'Shapes and Designs', 'Fun with Give and Take', 'Time Goes On', 'Who is Heavier?', 'How Many Times?', 'Play with Patterns', 'Jugs and Mugs', 'Can We Share?', 'Smart Charts!', 'Rupees and Paise'],
            'EVS': ['Poonam’s Day Out', 'The Plant Fairy', 'Water O’ Water!', 'Our First School', 'Chhotu’s House', 'Foods We Eat', 'Saying without Speaking', 'Flying High', 'It’s Raining', 'What is Cooking', 'From Here to There', 'Work We Do', 'Sharing Our Feelings', 'The Story of Food', 'Making Pots', 'Games We Play', 'Here comes a Letter', 'A House Like This', 'Our Friends - Animals', 'Drop by Drop', 'Families can be Different', 'Left-Right', 'A Beautiful Cloth', 'Web of Life'],
            'English': ['Good Morning', 'The Magic Garden', 'Bird Talk', 'Nina and the Baby Sparrows', 'Little by Little', 'The Enormous Turnip', 'Sea Song', 'A Little Fish Story', 'The Balloon Man', 'The Yellow Butterfly', 'Trains', 'The Story of the Road', 'Puppy and I', 'Little Tiger Big Tiger', 'He is My Brother', 'How Creatures Move', 'The Ship of the Desert'],
            'Hindi': ['Kakku', 'Shekhibaaz Makkhi', 'Chand Wali Amma', 'Man Karta Hai', 'Bahadur Bitto', 'Hamse Sab Kahte', 'Tiptipwa', 'Bandar Bant', 'Akal Badi Ya Bhains', 'Meera Bahan Aur Bagh', 'Jab Mujhe Saanp Ne Kata', 'Mirch Ka Maza', 'Sabse Achha Ped']
        },
        'Class 2': {
            'Maths': ['What is Long, What is Round?', 'Counting in Groups', 'How Much Can You Carry?', 'Counting in Tens', 'Patterns', 'Footprints', 'Jugs and Mugs', 'Tens and Ones', 'My Funday', 'Add Our Points', 'Lines and Lines', 'Give and Take', 'The Longest Step', 'Birds Come, Birds Go', 'How Many Ponytails?'],
            'English': ['First Day at School', 'Haldi’s Adventure', 'I am Lucky!', 'I Want', 'A Smile', 'The Wind and the Sun', 'Rain', 'Storm in the Garden', 'Zoo Manners', 'Funny Bunny', 'Mr. Nobody', 'Curlylocks and the Three Bears', 'On My Blackboard I can Draw', 'Make it Shorter', 'I am the Music Man', 'The Mumbai Musicians', 'Granny Granny Please Comb my Hair', 'The Magic Porridge Pot', 'Strange Talk', 'The Grasshopper and the Ant'],
            'Hindi': ['Oont Chala', 'Bhalu ne Kheli Football', 'Myaun Myaun', 'Adhik Balwan Kaun?', 'Dost ki Madad', 'Bahut Hua', 'Meri Kitaab', 'Titli aur Kali', 'Bulbul', 'Meethi Sarangi', 'Tesu Raja Beech Bazar', 'Bus ke neeche Bagh', 'Suraj Jaldi Aana Ji', 'Natkhat Chuha', 'Ekki-Dokki']
        },
        'Class 1': {
            'Maths': ['Shapes and Space', 'Numbers from One to Nine', 'Addition', 'Subtraction', 'Numbers from Ten to Twenty', 'Time', 'Measurement', 'Numbers from Twenty-one to Fifty', 'Data Handling', 'Patterns', 'Numbers', 'Money', 'How Many'],
            'English': ['A Happy Child', 'Three Little Pigs', 'After a Bath', 'The Bubble, the Straw and the Shoe', 'One Little Kitten', 'Lalu and Peelu', 'Once I Saw a Little Bird', 'Mittu and the Yellow Mango', 'Merry-Go-Round', 'Circle', 'If I Were an Apple', 'Our Tree', 'A Kite', 'Sundari', 'A Little Turtle', 'The Tiger and the Mosquito', 'Clouds', 'Anandi’s Rainbow', 'Flying-Man', 'The Tailor and his Friend'],
            'Hindi': ['Jhoola', 'Aam ki Kahani', 'Aam ki Tokari', 'Patte hi Patte', 'Pakodi', 'Chhuk-Chhuk Gadi', 'Rasoi Ghar', 'Chuho! Myau So Rahi Hai', 'Makdi-Kakdi-Lakdi', 'Pugdi', 'Patang', 'Gend-Balla', 'Bandar Gaya Khet Me Bhag', 'Ek Budhiya', 'Main Bhi', 'Lalu Aur Peelu']
        }
    }

    for grade_name, subjects in cbse_data.items():
        if grade_name == 'JEE':
            grade_num = 13
        elif grade_name == 'NEET':
            grade_num = 14
        elif grade_name == 'NDA':
            grade_num = 15
        else:
            grade_num = int(grade_name.replace('Class ', ''))
        grade, created = Grade.objects.get_or_create(
            name=grade_name,
            slug=slugify(grade_name),
            defaults={'order': grade_num}
        )
        print(f"Created Curriculum for {grade_name}")

        for sub_name, chapters in subjects.items():
            subject, _ = Subject.objects.get_or_create(
                grade=grade,
                name=sub_name,
                slug=slugify(sub_name),
                defaults={'icon': get_icon_for_subject(sub_name)}
            )
            
            for index, chapter_name in enumerate(chapters, 1):
                chapter = Chapter.objects.create(
                    subject=subject,
                    name=chapter_name,
                    slug=slugify(chapter_name),
                    order=index
                )
                
                Video.objects.create(
                    chapter=chapter,
                    title=f"Full Lesson: {chapter_name}",
                    youtube_id="dQw4w9WgXcQ",
                    description=f"In this high-quality educational video, we cover the essentials of CBSE {grade_name} {sub_name} Chapter {index}: {chapter_name}.",
                    order=1
                )
    
    print("Success! Ultimate complete CBSE standard courses populated for all 12 Classes along with JEE, NEET, and NDA.")

def get_icon_for_subject(name):
    icons = {
        'Maths': 'calculator',
        'Science': 'beaker',
        'English': 'book',
        'Hindi': 'languages',
        'EVS': 'leaf',
        'Social Science': 'globe',
        'Information Technology': 'cpu',
        'Sanskrit': 'pen-tool',
        'Physics': 'zap',
        'Chemistry': 'flask-conical',
        'Biology': 'dna',
        'Accountancy': 'pie-chart',
        'Business Studies': 'briefcase',
        'Economics': 'trending-up',
        'Computer Science': 'monitor',
    }
    return icons.get(name, 'book-open')

if __name__ == '__main__':
    populate_with_ultimate_cbse_data()
