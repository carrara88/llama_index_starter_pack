const embedding = async (embedding: string, authKey=''): Promise<any> => {
  const formData = new FormData();
  formData.append('llm_type', 'cloud'); // or 'local'
  formData.append('embedding', embedding);
  formData.append('auth_key', authKey);

  const requestURL = new URL('http://localhost:5601/embedding');
  const response = await fetch(requestURL, { mode: 'cors', body: formData, method: 'POST' });
  if (!response.ok) {
    return { text: 'Error in embedding', sources: [] };
  }

  const jsonResponse = (await response.json());
  return jsonResponse;
};

export default embedding;
