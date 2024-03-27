const { href } = VM.require("devhub.near/widget/core.lib.url");
const listLink = href({
  widgetSrc: `near/widget/AI.Nexus`,
});

const [question, setQuestion] = useState("");
const [loading, setLoading] = useState(false);
const [messages, setMessages] = useState([]);
const [settingsOpen, setSettingsOpen] = useState(false);
const [credential, setCredential] = useState(storedCredential ?? "");

const { src, embedded } = props;

const [accountId, agentType, agentName] = src.split("/") ?? [null, null, null];
const blockHeight = blockHeight ?? "final";

const data = Social.getr(`${accountId}/agent/${agentName}`, blockHeight);
const agent = { accountId, name: agentName, ...data };

if (!data) return "Loading...";

const toggleSettings = () => {
  setSettingsOpen(!settingsOpen);
};

useEffect(() => {
  Storage.set("agent-credential", credential);
}, [credential]);

const submitQuestion = () => {
  setLoading(true);
  asyncFetch("https://backend.denver-eth.assisterr.ai/chat-completion", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "OpenAI-API-Key": credential,
    },
    responseType: "json",
    body: JSON.stringify({
      prompt: question,
    }),
  })
    .then((response) => {
      if (response.status === 200) {
        const answer = response.body.response;
        setMessages(answer);
        return answer;
      } else {
        throw new Error(`Request failed with status ${response.status}`);
      }
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    })
    .finally(() => {
      setLoading(false);
      setQuestion("");
    });
};

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: 48px;
  padding: 48px;
`;

const Overview = styled.div`
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 1em;
`;

const Header = styled.h1`
  font-size: 24px;
  line-height: 39px;
  color: #11181c;
  margin-bottom: 20px;
  font-weight: 600;
`;
const Text = styled.p`
  margin: 0;
  font-size: 14px;
  line-height: 20px;
  color: ${(p) => (p.bold ? "#11181C" : "#687076")};
  font-weight: ${(p) => (p.bold ? "600" : "400")};
  font-size: ${(p) => (p.small ? "12px" : "14px")};

  i {
    margin-right: 4px;
  }
`;
const Prompt = styled.p`
  font-family: monospace;
  font-size: 14px;
  overflow-y: auto;
  height: 100px;
`;
const Label = styled.span`
  font-weight: 600;
`;
const Settings = styled.div`
  margin-bottom: 1em;
  z-index: 1000;
`;
const Controls = styled.div`
  margin-bottom: 1em;
`;
const CardControl = styled.div`
  cursor: pointer;
  color: var(--violet8);
  margin-bottom: 1em;
`;
const AllSettings = styled.div``;
const InputWrapper = styled.div`
  padding-bottom: 1em;
`;
const Question = styled.input`
  border-top-left-radius: 2rem;
  border-bottom-left-radius: 2rem;
`;
const UserMessage = styled.div``;
const AgentMessage = styled.div`
  background-color: #f9f9f9;
`;

const renderSettings = () => {
  return (
    <Settings>
      <CardControl bold onClick={toggleSettings}>
        <i className={settingsOpen ? "ph ph-caret-up" : "ph ph-caret-down"} />{" "}
        Settings
      </CardControl>
      {settingsOpen && (
        <AllSettings>
          <InputWrapper>
            <div className="row">
              <div className="col">
                <Widget
                  src="near/widget/DIG.Input"
                  props={{
                    label: "Credentials",
                    assistiveText:
                      "Your OpenAI API Key or other credentials, will be stored in your browser.",
                    iconLeft: "ph-bold ph-identification-card",
                    onInput: (e) => setCredential(e.target.value),
                    value: credential,
                    type: "password",
                  }}
                />
              </div>
            </div>
          </InputWrapper>
        </AllSettings>
      )}
    </Settings>
  );
};

return (
  <Wrapper>
    <div>
      {!embedded && (
        <div>
          <Link to={listLink}>
            <Header>
              <i className="ph ph-arrow-left" />
              Agent List
            </Header>
          </Link>
          <Overview>
            <div className="row">
              <div className="col-5">
                <Widget
                  src="near/widget/AI.Agent.AgentSummary"
                  props={{
                    size: "small",
                    showTags: true,
                    agent: agent,
                  }}
                />
              </div>
              <div className="col-7">
                <Prompt>
                  <Label>Description:</Label> <Markdown text={data.prompt} />
                </Prompt>
              </div>
            </div>
          </Overview>
        </div>
      )}
      <Controls>
        <div className="input-group">
          <Question
            type="text"
            className="form-control"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === "Enter") {
                submitQuestion();
              }
            }}
            placeholder="What's your question?"
            autoFocus
          />
          <Widget
            src="near/widget/DIG.Button"
            props={{
              onClick: submitQuestion,
              iconLeft: editIcon,
              variant: "affirmative",
              fill: "solid",
              size: "large",
              label: "Submit",
              disabled: credential === "",
              style: {
                borderTopLeftRadius: "0rem",
                borderBottomLeftRadius: "0rem",
              },
            }}
          />
        </div>
      </Controls>
      {renderSettings()}
      {messages && <Markdown text={messages} />}
      <div className="d-flex flex-column-reverse">
        {loading && (
          <div key="loading" className={`message system`}>
            <div>
              <span
                className="spinner-grow spinner-grow-sm me-1"
                role="status"
                aria-hidden="true"
              />
            </div>
          </div>
        )}
      </div>
    </div>
  </Wrapper>
);
