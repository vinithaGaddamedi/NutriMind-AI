import axios from 'axios';

export const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
});

export const sendChatMessage = async (message, conversationId = null, userContext = {}) => {
  const response = await apiClient.post('/chat/', {
    message,
    conversation_id: conversationId,
    user_context: userContext
  });
  return response.data;
};
