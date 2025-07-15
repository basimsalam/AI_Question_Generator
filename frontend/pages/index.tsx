import { useState } from 'react';
import type { GeneratePaperRequest, GeneratePaperResponse } from '../types/question';

const Home = () => {
  const [formData, setFormData] = useState<GeneratePaperRequest>({
    subject: '',
    grade: '',
    topics: [],
    difficulty_distribution: {
      Easy: 0,
      Medium: 0,
      Hard: 0,
    },
    question_types: [],
  });

  const [paper, setPaper] = useState<GeneratePaperResponse['body'] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [topicInput, setTopicInput] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/generate-paper`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data: GeneratePaperResponse = await res.json();
      if (data.status === 'success') {
        setPaper(data.body);
      } else {
        setError(data.message);
      }
    } catch (err) {
      setError('Failed to connect to backend.');
    } finally {
      setLoading(false);
    }
  };

  const addTopic = () => {
    if (topicInput.trim()) {
      setFormData({ ...formData, topics: [...formData.topics, topicInput.trim()] });
      setTopicInput('');
    }
  };

  const toggleQuestionType = (type: string) => {
    const exists = formData.question_types.includes(type);
    setFormData({
      ...formData,
      question_types: exists
        ? formData.question_types.filter((t) => t !== type)
        : [...formData.question_types, type],
    });
  };

  return (
    <div className="min-h-screen bg-gray-100 py-10 px-4">
      <div className="max-w-3xl mx-auto bg-white rounded shadow-md p-8">
        <h1 className="text-2xl font-bold mb-6">AI Question Paper Generator</h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block font-medium">Subject:</label>
            <input
              type="text"
              value={formData.subject}
              onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
              required
              className="mt-1 w-full border px-3 py-2 rounded"
            />
          </div>

          <div>
            <label className="block font-medium">Grade:</label>
            <input
              type="text"
              value={formData.grade}
              onChange={(e) => setFormData({ ...formData, grade: e.target.value })}
              required
              className="mt-1 w-full border px-3 py-2 rounded"
            />
          </div>

          <div>
            <label className="block font-medium">Topics:</label>
            <div className="flex space-x-2">
              <input
                type="text"
                value={topicInput}
                onChange={(e) => setTopicInput(e.target.value)}
                className="flex-1 border px-3 py-2 rounded"
              />
              <button type="button" onClick={addTopic} className="bg-blue-500 text-white px-4 py-2 rounded">Add Topic</button>
            </div>
            <ul className="list-disc list-inside mt-2 text-sm text-gray-700">
              {formData.topics.map((t, idx) => <li key={idx}>{t}</li>)}
            </ul>
          </div>

          <div>
            <label className="block font-medium">Question Types:</label>
            <div className="flex space-x-4 mt-1">
              {['MCQ', 'Short Answer', 'Long Answer'].map((type) => (
                <label key={type} className="inline-flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.question_types.includes(type)}
                    onChange={() => toggleQuestionType(type)}
                    className="mr-2"
                  /> {type}
                </label>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4">
            {['Easy', 'Medium', 'Hard'].map((level) => (
              <div key={level}>
                <label className="block font-medium">{level} Questions:</label>
                <input
                  type="number"
                  value={formData.difficulty_distribution[level as keyof typeof formData.difficulty_distribution]}
                  onChange={(e) => setFormData({
                    ...formData,
                    difficulty_distribution: {
                      ...formData.difficulty_distribution,
                      [level]: Number(e.target.value),
                    },
                  })}
                  className="mt-1 w-full border px-3 py-2 rounded"
                />
              </div>
            ))}
          </div>

          <button
            type="submit"
            disabled={loading}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            {loading ? 'Generating...' : 'Generate Paper'}
          </button>
        </form>

        {error && <p className="text-red-600 mt-4">{error}</p>}

        {paper && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold mb-2">Generated Questions</h2>
            <ul className="list-disc list-inside space-y-2">
              {Object.entries(paper.paper).map(([key, val]) => (
                <li key={key}><strong>{key}</strong>: {val}</li>
              ))}
            </ul>

            <h3 className="mt-6 font-medium">Download</h3>
            <div className="space-x-4 mt-2">
              <a href={`${process.env.NEXT_PUBLIC_API_URL}${paper.download_links.pdf}`} target="_blank" className="text-blue-600 underline">Download PDF</a>
              <a href={`${process.env.NEXT_PUBLIC_API_URL}${paper.download_links.word}`} target="_blank" className="text-blue-600 underline">Download Word</a>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;