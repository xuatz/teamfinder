import React, { Component, PropTypes } from 'react'

import { withTeam } from 'components/connectors/WithTeam'

class TeamName extends Component {

    static propTypes = {
        teamId: PropTypes.string.isRequired
    }

    render() {
        const { team: { team } } = this.props
        return <span>{team && team.name}</span>
    }

}

TeamName = withTeam(props => props.teamId)(TeamName)

export default TeamName
