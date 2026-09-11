const express = require('express');
const crypto = require('crypto');
// const ExcelJS = require('exceljs'); // Удалено
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// SHA-256 hash
function hashInput(input) {
    return crypto.createHash('sha256').update(input).digest('hex');
}

// Measure performance
function measurePerformance(input) {
    const startTime = process.hrtime();
    const hash = hashInput(input);
    const endTime = process.hrtime(startTime);
    const executionTime = (endTime[0] * 1000 + endTime[1] / 1000000); // ms
    return { hash, executionTime };
}

// API: Hash input
app.post('/api/hash', (req, res) => {
    const { input } = req.body;
    if (typeof input !== 'string') return res.status(400).json({ error: 'Input required' });
    const result = measurePerformance(input);
    res.json(result);
});

// API: Performance test
app.post('/api/performance', (req, res) => {
    const { input, startLength, stepLength, iterations, samples } = req.body;
    if (typeof input !== 'string' || typeof iterations !== 'number' || typeof startLength !== 'number' || typeof stepLength !== 'number' || typeof samples !== 'number') {
        return res.status(400).json({ error: 'Input, startLength, stepLength, iterations, samples required' });
    }
    const results = [];
    for (let i = 0; i < iterations; i++) {
        const len = startLength + i * stepLength;
        let testInput = input.repeat(Math.ceil(len / input.length)).slice(0, len);
        let sum = 0;
        for (let j = 0; j < samples; j++) {
            const result = measurePerformance(testInput);
            sum += result.executionTime;
        }
        const avgTime = sum / samples;
        results.push({
            iteration: i + 1,
            inputLength: len,
            executionTime: avgTime
        });
    }
    res.json(results);
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
}); 