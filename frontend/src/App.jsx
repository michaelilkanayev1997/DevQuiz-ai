import { Route, Routes } from "react-router-dom";

import "./App.css";
import ClerkProviderWithRoutes from "./auth/ClerkProviderWithRoutes";
import AuthenticationPage from "./auth/AuthenticationPage";
import Layout from "./layout/Layout";
import ChallengeGenerator from "./challenge/ChallengeGenerator";
import HistoryPanel from "./history/HistoryPanel";

function App() {
  return (
    <ClerkProviderWithRoutes>
      <Routes>
        <Route path="/sign-in/*" element={<AuthenticationPage />} />
        <Route path="/sign-up" element={<AuthenticationPage />} />
        <Route element={<Layout />}>
          <Route path="/" element={<ChallengeGenerator />} />
          <Route path="/history" element={<HistoryPanel />} />
        </Route>
      </Routes>
    </ClerkProviderWithRoutes>
  );
}

export default App;
