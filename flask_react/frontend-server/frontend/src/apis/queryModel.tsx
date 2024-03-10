export type ResponseSources = {
  text: string;
  doc_id: string;
  start: number;
  end: number;
  similarity: number;
};

export type QueryResponse = {
  text: string;
  sources: ResponseSources[];
};

const queryModel = async (query: string, authKey=''): Promise<QueryResponse> => {
  const formData = new FormData();
  formData.append('llm_type', 'cloud'); // or 'local'
  formData.append('query', query);
  if (authKey) formData.append('auth_key', authKey);

  const requestURL = new URL('http://localhost:5601/query_model');
  const response = await fetch(requestURL, { mode: 'cors', body: formData, method: 'POST' });
  if (!response.ok) {
    return { text: 'Error in query', sources: [] };
  }

  const jsonResponse = (await response.json()) as QueryResponse;
  return jsonResponse;
};

export default queryModel;
