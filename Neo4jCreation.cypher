// Create Muscle nodes
UNWIND [
    "quads", "hams", "glutes", "chest", "back", "delts", "rear delts", "front delts",
    "biceps", "triceps", "traps", "calves", "abs", "forearms", "abductor"
] AS muscle
CREATE (:Muscle {name: muscle});

// Create Exercise nodes
UNWIND [
    "bench press", "incline bench press", "squat", "deadlift", "overhead press", "pull-up", "chin-up",
    "barbell row", "dumbbell fly", "bicep curl", "tricep extension", "lunges", "leg press", "calf raise",
    "plank", "crunch", "hamstring curl", "front raise", "lateral raise", "face pull", "shrugs",
    "reverse fly", "cable pulldown", "lat pulldown", "hanging leg raise", "ab roller", "farmer's carry",
    "side plank", "hip thrust", "cable crossover", "t-bar row", "seated row", "cable curl", "preacher curl",
    "dumbbell pullover", "romanian deadlift", "glute bridge", "split squat", "peck deck", "tricep dips",
    "kettlebell swing", "snatch", "clean and jerk", "mountain climbers", "pike push-up", "skullcrushers",
    "seated calf raise", "hang clean", "abductor side lift", "abductor squat", "dumbbell abductor lunge",
    "standing abductor raise"
] AS exercise
CREATE (:Exercise {name: exercise});

// Create requirement nodes
UNWIND [
    "none", "dumbbells", "barbell", "machine", "cable", "smith machine"
] AS requirement
CREATE (:Requirement {name: requirement});

// Create distribution nodes
UNWIND [
    "push, pull, legs", "arnold split", "bro split", "full body"
] AS distribution
CREATE (:Distribution {name: distribution});

// Create group nodes
UNWIND [
    {group: "push", muscles: ["chest", "triceps", "front delts", "delts"]},
    {group: "pull", muscles: ["back", "traps", "biceps", "rear delts", "forearms"]},
    {group: "legs", muscles: ["quads", "hams", "glutes", "calves", "abs", "abductor"]},
    {group: "arnold push", muscles: ["chest", "biceps", "front delts", "delts"]},
    {group: "arnold pull", muscles: ["back", "traps", "triceps", "rear delts", "forearms"]},
    {group: "arnold legs", muscles: ["quads", "hams", "glutes", "calves", "abs", "abductor"]},
    {group: "bro chest", muscles: ["chest"]},
    {group: "bro back", muscles: ["back"]},
    {group: "bro arms", muscles: ["biceps", "triceps", "forearms"]},
    {group: "bro shoulder", muscles: ["delts", "traps", "front delts", "rear delts"]},
    {group: "bro legs", muscles: ["quads", "hams", "glutes", "calves", "abs", "abductor"]},
    {group: "full body", muscles: ["quads", "hams", "glutes", "chest", "back", "delts", "rear delts", "front delts",
    "biceps", "triceps", "traps", "calves", "abs", "forearms", "abductor"]}
] AS groupData
CREATE (g:Group {name: groupData.group})
WITH g, groupData.muscles AS muscles
UNWIND muscles AS muscle
MATCH (m:Muscle {name: muscle})
MERGE (g)-[:INCLUDES]->(m);

// Relate distributions to groups
UNWIND [
    {distribution: "push, pull, legs", groups: ["push", "pull", "legs"]},
    {distribution: "arnold split", groups: ["arnold push", "arnold pull", "arnold legs"]},
    {distribution: "bro split", groups: ["bro chest", "bro back", "bro arms", "bro shoulder", "bro legs"]},
    {distribution: "full body", groups: ["full body"]}
] AS distributionData
MATCH (d:Distribution {name: distributionData.distribution})
UNWIND distributionData.groups AS group
MATCH (g:Group {name: group})
MERGE (d)-[:USES]->(g);

// Create relationships between exercises and muscles, with requirement
UNWIND [
    {exercise: "bench press", muscles: {direct: ["chest"], indirect: ["front delts", "triceps"]}, requirement: ["barbell", "dumbbells"]},
    {exercise: "incline bench press", muscles: {direct: ["chest"], indirect: ["front delts", "triceps"]}, requirement: ["barbell", "dumbbells"]},
    {exercise: "squat", muscles: {direct: ["quads", "glutes"], indirect: ["hams", "calves"]}, requirement: ["barbell", "smith machine"]},
    {exercise: "deadlift", muscles: {direct: ["back", "glutes"], indirect: ["hams", "traps", "forearms"]}, requirement: ["barbell"]},
    {exercise: "overhead press", muscles: {direct: ["delts"], indirect: ["triceps", "traps"]}, requirement: ["barbell", "dumbbells"]},
    {exercise: "pull-up", muscles: {direct: ["back"], indirect: ["biceps", "traps"]}, requirement: ["none"]},
    {exercise: "chin-up", muscles: {direct: ["back"], indirect: ["biceps", "forearms"]}, requirement: ["none"]},
    {exercise: "barbell row", muscles: {direct: ["back"], indirect: ["biceps", "rear delts"]}, requirement: ["barbell"]},
    {exercise: "dumbbell fly", muscles: {direct: ["chest"], indirect: ["front delts"]}, requirement: ["dumbbells"]},
    {exercise: "bicep curl", muscles: {direct: ["biceps"], indirect: ["forearms"]}, requirement: ["dumbbells", "cable"]},
    {exercise: "tricep extension", muscles: {direct: ["triceps"], indirect: []}, requirement: ["dumbbells", "cable"]},
    {exercise: "lunges", muscles: {direct: ["quads", "glutes"], indirect: ["calves"]}, requirement: ["dumbbells"]},
    {exercise: "leg press", muscles: {direct: ["quads", "glutes"], indirect: []}, requirement: ["machine"]},
    {exercise: "calf raise", muscles: {direct: ["calves"], indirect: []}, requirement: ["dumbbells", "machine"]},
    {exercise: "plank", muscles: {direct: ["abs"], indirect: []}, requirement: ["none"]},
    {exercise: "crunch", muscles: {direct: ["abs"], indirect: []}, requirement: ["none"]},
    {exercise: "hamstring curl", muscles: {direct: ["hams"], indirect: []}, requirement: ["machine"]},
    {exercise: "front raise", muscles: {direct: ["front delts"], indirect: []}, requirement: ["dumbbells"]},
    {exercise: "lateral raise", muscles: {direct: ["delts"], indirect: []}, requirement: ["dumbbells"]},
    {exercise: "face pull", muscles: {direct: ["rear delts"], indirect: ["traps"]}, requirement: ["cable"]},
    {exercise: "shrugs", muscles: {direct: ["traps"], indirect: []}, requirement: ["dumbbells", "barbell"]},
    {exercise: "reverse fly", muscles: {direct: ["rear delts"], indirect: ["back"]}, requirement: ["dumbbells"]},
    {exercise: "cable pulldown", muscles: {direct: ["back"], indirect: ["biceps"]}, requirement: ["cable"]},
    {exercise: "lat pulldown", muscles: {direct: ["back"], indirect: ["biceps"]}, requirement: ["cable"]},
    {exercise: "hanging leg raise", muscles: {direct: ["abs"], indirect: []}, requirement: ["none"]},
    {exercise: "ab roller", muscles: {direct: ["abs"], indirect: []}, requirement: ["none"]},
    {exercise: "farmer's carry", muscles: {direct: ["forearms"], indirect: ["traps", "core"]}, requirement: ["dumbbells", "kettlebell"]},
    {exercise: "side plank", muscles: {direct: ["abs"], indirect: ["obliques"]}, requirement: ["none"]},
    {exercise: "hip thrust", muscles: {direct: ["glutes"], indirect: ["hams"]}, requirement: ["barbell", "machine"]},
    {exercise: "cable crossover", muscles: {direct: ["chest"], indirect: []}, requirement: ["cable"]},
    {exercise: "t-bar row", muscles: {direct: ["back"], indirect: ["biceps"]}, requirement: ["machine"]},
    {exercise: "seated row", muscles: {direct: ["back"], indirect: ["biceps"]}, requirement: ["cable", "machine"]},
    {exercise: "cable curl", muscles: {direct: ["biceps"], indirect: []}, requirement: ["cable"]},
    {exercise: "preacher curl", muscles: {direct: ["biceps"], indirect: []}, requirement: ["barbell", "dumbbells"]},
    {exercise: "dumbbell pullover", muscles: {direct: ["chest"], indirect: ["back"]}, requirement: ["dumbbells"]},
    {exercise: "romanian deadlift", muscles: {direct: ["hams"], indirect: ["glutes", "lower back"]}, requirement: ["barbell", "dumbbells"]},
    {exercise: "glute bridge", muscles: {direct: ["glutes"], indirect: ["hams"]}, requirement: ["none"]},
    {exercise: "split squat", muscles: {direct: ["quads", "glutes"], indirect: []}, requirement: ["dumbbells"]},
    {exercise: "peck deck", muscles: {direct: ["chest"], indirect: []}, requirement: ["machine"]},
    {exercise: "tricep dips", muscles: {direct: ["triceps"], indirect: ["chest"]}, requirement: ["none"]},
    {exercise: "kettlebell swing", muscles: {direct: ["glutes", "hams"], indirect: ["back"]}, requirement: ["kettlebell"]},
    {exercise: "snatch", muscles: {direct: ["delts"], indirect: ["traps", "glutes"]}, requirement: ["barbell", "kettlebell"]},
    {exercise: "clean and jerk", muscles: {direct: ["delts", "quads"], indirect: ["traps", "glutes"]}, requirement: ["barbell"]},
    {exercise: "mountain climbers", muscles: {direct: ["abs"], indirect: ["quads"]}, requirement: ["none"]},
    {exercise: "pike push-up", muscles: {direct: ["delts"], indirect: ["triceps"]}, requirement: ["none"]},
    {exercise: "skullcrushers", muscles: {direct: ["triceps"], indirect: []}, requirement: ["barbell", "dumbbells"]},
    {exercise: "seated calf raise", muscles: {direct: ["calves"], indirect: []}, requirement: ["machine"]},
    {exercise: "hang clean", muscles: {direct: ["traps", "delts"], indirect: ["quads"]}, requirement: ["barbell"]},
    {exercise: "abductor side lift", muscles: {direct: ["abductor"], indirect: []}, requirement: ["dumbbells"]},
    {exercise: "abductor squat", muscles: {direct: ["abductor"], indirect: []}, requirement: ["dumbbells"]},
    {exercise: "dumbbell abductor lunge", muscles: {direct: ["abductor"], indirect: []}, requirement: ["dumbbells"]},
    {exercise: "standing abductor raise", muscles: {direct: ["abductor"], indirect: []}, requirement: ["dumbbells"]}
] AS data
MATCH (e:Exercise {name: data.exercise})
UNWIND keys(data.muscles) AS type
UNWIND data.muscles[type] AS muscle
MATCH (m:Muscle {name: muscle})
WITH e, m, type, data
FOREACH (_ IN CASE WHEN type = "direct" THEN [1] ELSE [] END |
    MERGE (e)-[:WORKS_DIRECTLY]->(m)
)
FOREACH (_ IN CASE WHEN type = "indirect" THEN [1] ELSE [] END |
    MERGE (e)-[:WORKS_INDIRECTLY]->(m)
)
WITH e, data
UNWIND data.requirement AS req
MATCH (r:Requirement {name: req})
MERGE (e)-[:REQUIRES]->(r);
