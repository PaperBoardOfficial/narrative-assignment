import styled from "styled-components";

const StyledMessage = styled.p<{ color: string }>`
  color: ${(props) => props.color};
`;

export default StyledMessage;