export type Document = {
  id: string;
  text: string;
};

const fetchDocuments = async (authKey=''): Promise<Document[]> => {
  const formData = new FormData();
  formData.append('llm_type', 'cloud'); // or 'local'
  formData.append('auth_key', authKey);
  const response = await fetch('http://localhost:5601/get_documents_list', { mode: 'cors' });

  if (!response.ok) {
    return [];
  }

  const jsonResponse = (await response.json()) as Document[];
  return jsonResponse;
};

export default fetchDocuments;
