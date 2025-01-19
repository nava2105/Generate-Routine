CREATE SCHEMA ptrainer_volumes;

CREATE TABLE ptrainer_volumes.training_volumes (
    muscle_group VARCHAR(20),
    mv INT,           		-- Maintenance Volume
    mev INT,          		-- Effective Volume
    mav INT,          		-- Adaptive Volume
    mrv INT,          		-- Maximum Recoverable Volume
    frequency_per_week FLOAT, 	-- Frequency per week
    reps INT,     		-- Repetitions
    rir INT      		-- Minimum Reps in Reserve
);

INSERT INTO ptrainer_volumes.training_volumes (muscle_group, mv, mev, mav, mrv, frequency_per_week, reps, rir) VALUES
('quads', 6, 10, 16, 20, 2.25, 13, 2),
('hams', 4, 8, 13, 20, 2.5, 13, 2),
('glutes', 0, 2, 8, 16, 2.5, 13, 2),
('chest', 8, 11, 16, 22, 3, 13, 2),
('back', 8, 12, 18, 25, 3, 13, 2),
('delts', 3, 7, 19, 26, 4, 14, 1),
('rear delts', 3, 7, 19, 26, 4, 14, 1),
('front delts', 3, 7, 19, 26, 4, 14, 1),
('biceps', 3, 11, 17, 26, 4, 12, 1),
('triceps', 2, 8, 12, 18, 3, 19, 1),
('traps', 0, 7, 16, 26, 4, 19, 1),
('calves', 3, 10, 14, 20, 3, 19, 1),
('abs', 0, 8, 18, 25, 4, 19, 1),
('forearms', 0, 6, 12, 18, 3, 12, 1),
('abductor', 0, 5, 10, 14, 3, 10, 2);